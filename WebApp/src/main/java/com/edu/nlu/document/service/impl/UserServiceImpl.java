package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.enums.Role;
import com.edu.nlu.document.model.Department;
import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.model.Statement;
import com.edu.nlu.document.model.User;
import com.edu.nlu.document.repository.UserRepository;
import com.edu.nlu.document.service.CommonService;
import com.edu.nlu.document.service.DepartmentService;
import com.edu.nlu.document.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final CommonService commonService;
    private final DepartmentService deparmentService;


    @Override
    public List<User> findAll() {
        Role role = commonService.getCurrentUserRole();
        if (role == Role.BAN_GIAM_DOC){
            List<Department> departments = deparmentService.getAllDepartments();
            List<User> users = new ArrayList<>();

            for (Department department : departments) {
                users.add(userRepository.getReferenceById(department.getHostId()));
            }
            return users;
        }
        else if(role == Role.CHUYEN_VIEN){
            User userCurrent = userRepository.getReferenceById(commonService.getCurrentUserId());
            return userRepository.findAllByDepartmentId(userCurrent.getDepartmentId());
        }
        Role roleMustFind = switch (role) {
            case VAN_THU -> Role.CHANH_VAN_PHONG;
            case CHANH_VAN_PHONG -> Role.BAN_GIAM_DOC;
            default -> throw new IllegalStateException("Unexpected role: " + role);
        };

        return userRepository.findAllByRole(roleMustFind.name());
    }

    @Override
    public User findByUsername(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }

    @Override
    public User findById(Long id) {
        return userRepository.findById(id).orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }

    @Override
    public List<User> getAllUserSender(List<Statement> statementsList) {
        List<Long> idSender = new ArrayList<>();
        for (Statement statement : statementsList) {
            idSender.add(statement.getSenderId());
        }
        List<User> users = new ArrayList<>();
        for (Long id : idSender) {
            users.add(findById(id));
        }
        return users;
    }
}
