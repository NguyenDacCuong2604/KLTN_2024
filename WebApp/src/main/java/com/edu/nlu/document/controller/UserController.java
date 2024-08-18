package com.edu.nlu.document.controller;

import com.edu.nlu.document.config.GeneralProperties;
import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.model.File;
import com.edu.nlu.document.model.Statement;
import com.edu.nlu.document.model.User;
import com.edu.nlu.document.model.Department;
import com.edu.nlu.document.payload.DocumentDetails;
import com.edu.nlu.document.payload.DocumentForm;
import com.edu.nlu.document.payload.UserDetails;
import com.edu.nlu.document.service.DepartmentService;
import com.edu.nlu.document.service.DocumentService;
import com.edu.nlu.document.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Controller
@RequestMapping(path = "/users")
public class UserController {
    @Autowired
    private RestTemplate restTemplate;
    private final UserService userService;
    private final DepartmentService departmentService;
    private final DocumentService documentService;

    @Autowired
    private GeneralProperties generalProperties;


    @GetMapping
    public String showUserList(Model model) {
        List<User> users = userService.findAll();
        model.addAttribute("users", users);
        return "user-list";
    }

    @GetMapping(path = "/data")
    public @ResponseBody List<User> getUsers() {
        return userService.findAll();
    }

    @GetMapping(path = "/chanhvanphong")
    public @ResponseBody List<UserDetails> getChanhvanphong() {
        List<User> users = userService.findAll();
        List<UserDetails> usersDetails = new ArrayList<>();
        for (User user : users) {
            UserDetails userDetails = new UserDetails();
            Department department = departmentService.getDepartmentById(user.getDepartmentId());
            userDetails.setDepartment(department);
            userDetails.setUser(user);
            usersDetails.add(userDetails);
        }
        return usersDetails;
    }

    @GetMapping(path = "/bangiamdoc")
    public @ResponseBody List<UserDetails> getBangiamdoc() {
        List<User> users = userService.findAll();
        List<UserDetails> usersDetails = new ArrayList<>();
        for (User user : users) {
            UserDetails userDetails = new UserDetails();
            Department department = departmentService.getDepartmentById(user.getDepartmentId());
            userDetails.setDepartment(department);
            userDetails.setUser(user);
            usersDetails.add(userDetails);
        }
        return usersDetails;
    }

    @GetMapping(path = "/chuyenphongban/{id_doc}")
    public @ResponseBody List<UserDetails> getChuyenPhongBan(@PathVariable(name = "id_doc") Long id) {
        Document document = documentService.getDocumentById(id);
        String trichyeu = document.getTrichYeu();

        Map<String, String> requestBody = Map.of("text", trichyeu);

        List<UserDetails> usersDetails = new ArrayList<>();
        try {
            // Tạo đối tượng HttpEntity với body và headers
            HttpHeaders headers = new HttpHeaders();
            headers.set("Content-Type", "application/json");
            HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

            // Gửi yêu cầu POST và nhận phản hồi
            ResponseEntity<Map> responseEntity = restTemplate.exchange(
                    generalProperties.getExternalApiUrl(),
                    HttpMethod.POST,
                    requestEntity,
                    Map.class
            );

            // Lấy kết quả từ phản hồi
            Map<String, Object> responseBody = responseEntity.getBody();
            if (responseBody == null) {
                throw new RuntimeException("No response body from external API");
            }

            // Xử lý phản hồi
            List<Map<String, Double>> predictList = (List<Map<String, Double>>) responseBody.get("predict");
            if (predictList == null || predictList.isEmpty()) {
                throw new RuntimeException("Predict list is empty from external API");
            }

            // Giả sử danh sách chứa một bản đồ
            Map<String, Double> predictMap = predictList.get(0);

            List<User> users = userService.findAll();

            for (User user : users) {
                UserDetails userDetails = new UserDetails();
                Department department = departmentService.getDepartmentById(user.getDepartmentId());
                userDetails.setDepartment(department);
                userDetails.setUser(user);

                // Gán xác suất
                Double probability = predictMap.get(department.getNaturalId());
                if (probability != null) {
                    userDetails.setProbability(probability);

                    // Kiểm tra ngưỡng và thiết lập thuộc tính do_not_select
                    if (probability <= generalProperties.getThresholdMin()) {
                        userDetails.setDo_not_select(true);
                    } else {
                        userDetails.setDo_not_select(false);
                    }
                } else {
                    userDetails.setProbability(0.0); // hoặc một giá trị mặc định
                    userDetails.setDo_not_select(true); // Nếu không có xác suất, đặt do_not_select là true
                }

                usersDetails.add(userDetails);
            }

            // Sắp xếp theo xác suất giảm dần
            usersDetails.sort((ud1, ud2) -> Double.compare(ud2.getProbability(), ud1.getProbability()));

            // Cắt ngưỡng dựa trên hiệu xác suất
            double highestProbability = usersDetails.get(0).getProbability();
            for (int i = 0; i < usersDetails.size(); i++) {
                UserDetails userDetails = usersDetails.get(i);
                double currentProbability = userDetails.getProbability();

                // Kiểm tra xem hiệu xác suất có lớn hơn cut_threshold không
                if (highestProbability - currentProbability <= generalProperties.getCutThreshold()) {
                    userDetails.setPredict(true);
                    highestProbability = userDetails.getProbability();
                } else {
                    userDetails.setPredict(false);
                    break;
                }
            }

        } catch (Exception e) {
            // Xử lý lỗi và ghi log nếu cần thiết
            System.err.println("Error occurred while calling external API or processing data: " + e.getMessage());

            // Tiếp tục với danh sách người dùng mặc định nếu có lỗi
            List<User> users = userService.findAll();
            for (User user : users) {
                UserDetails userDetails = new UserDetails();
                Department department = departmentService.getDepartmentById(user.getDepartmentId());
                userDetails.setDepartment(department);
                userDetails.setUser(user);
                userDetails.setProbability(0.0); // Giá trị mặc định khi không có dữ liệu
                userDetails.setDo_not_select(true); // Giá trị mặc định khi không có dữ liệu
                userDetails.setPredict(false); // Giá trị mặc định cho isPredict
                usersDetails.add(userDetails);
            }
        }

        return usersDetails;
    }

    @GetMapping(path = "/phanCongPhongBan")
    public @ResponseBody List<UserDetails> getPhanCongPhongBan() {
        List<User> users = userService.findAll();
        List<UserDetails> usersDetails = new ArrayList<>();
        for (User user : users) {
            UserDetails userDetails = new UserDetails();
            Department department = departmentService.getDepartmentById(user.getDepartmentId());
            userDetails.setDepartment(department);
            userDetails.setUser(user);
            usersDetails.add(userDetails);
        }
        return usersDetails;
    }

}
