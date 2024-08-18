package com.edu.nlu.document.controller;

import com.edu.nlu.document.enums.Status;
import com.edu.nlu.document.mapper.DocumentMapper;
import com.edu.nlu.document.model.*;
import com.edu.nlu.document.payload.DocumentDetails;
import com.edu.nlu.document.payload.DocumentForm;
import com.edu.nlu.document.payload.DocumentForward;
import com.edu.nlu.document.payload.UserDetails;
import com.edu.nlu.document.service.*;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.parameters.P;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@Slf4j
@RequiredArgsConstructor
@Controller
@RequestMapping(path = "/documents")
public class DocumentController {
    private final DocumentMapper documentMapper;
    private final UserService userService;
    private final DocumentService documentService;
    private final FileService fileService;
    private final StatementService statementService;
    private final CommonService commonService;
    private final DepartmentService departmentService;
    private final DocumentLogService documentLogService;

    @GetMapping
    public String showUserList(Model model) {
        List<User> users = userService.findAll();
        model.addAttribute("users", users);
        return "user-list";
    }

    //Lấy thông tin Document từ id
    @GetMapping(path = "/{id}")
    public @ResponseBody DocumentDetails showDocumentDetails(@PathVariable(name = "id") Long id, Model model) {
        Document document = documentService.getDocumentById(id);
        DocumentForm documentForm = documentMapper.destinationToSource(document);
        List<File> files = fileService.getAllFileByDocumentId(id);
        Statement statement = statementService.getStatement(commonService.getCurrentUserId(), document.getId());
        List<DocumentLogWrapper> logs = documentLogService.getDocumentLogs(document.getId());

        DocumentDetails documentDetails = new DocumentDetails();
        documentDetails.setDocumentId(document.getId());
        documentDetails.setDocumentForm(documentForm);
        documentDetails.setFiles(files);
        documentDetails.setStatement(statement);
        documentDetails.setLogs(logs);

        return documentDetails;
    }

    //Tạo văn bản đến từ form
    @PostMapping(path = "/luuvanban")
    public String showXuLyVanBan( @RequestParam(defaultValue = "false") Boolean isLegalDocument,
                                  @RequestParam(defaultValue = "false") Boolean isDirectiveDocument,
                                  @RequestParam(defaultValue = "false") Boolean hasPaperCopy,
                                  @Valid @ModelAttribute DocumentForm documentForm, Model model) {
        documentForm.setIsLegalDocument(isLegalDocument);
        documentForm.setIsDirectiveDocument(isDirectiveDocument);
        documentForm.setHasPaperCopy(hasPaperCopy);
        System.out.println(documentForm.getAttachedFiles().get(0).getOriginalFilename());
        documentService.addNewDocument(documentForm); //Thêm document vào database
        return "tiepnhanvanbanden";
    }

    @PostMapping(path="/xoavanbanhanhchinh")
    public String xoaVanBan(@RequestParam("id") Long documentId){
        documentService.deleteDocument(documentId);
        return "redirect:/dashboard";
    }

    //Chuyển văn bản từ Văn thư sang chuyên viên
    @PostMapping(path = "/chuyenchuyenvien")
    public String showChuyenChuyenVien(@Valid @ModelAttribute DocumentForward documentForward, Model model) {
        Long currentUserId = commonService.getCurrentUserId();
        documentForward.getReceivedUsers().forEach(userId -> {
            //Log
            DocumentLog documentLog = new DocumentLog();
            documentLog.setCreatedBy(currentUserId);
            documentLog.setDocumentId(documentForward.getDocumentId());

            //Statement
            Statement newStatement = new Statement();
            newStatement.setDocumentId(documentForward.getDocumentId());
            newStatement.setNote(documentForward.getContent());
            newStatement.setUserId(userId);

            User userReceived = userService.findById(userId);
            Department departmentReceived = departmentService.getDepartmentById(userReceived.getDepartmentId());
            documentLog.setStatus("Đã chuyển văn bản đến người xử lý - "+departmentReceived.getName()+"("+userReceived.getPosition()+"-"+userReceived.getName()+")");
            newStatement.setStatus(Status.SENT); //Người xem và có thể xử lý

            newStatement.setSenderId(currentUserId);
            statementService.createStatement(newStatement);
            documentLogService.addDocumentLog(documentLog);

        });

        Statement storedStatement = statementService.getStatement(currentUserId, documentForward.getDocumentId());
        storedStatement.setStatus(Status.FORWARDED);
        statementService.updateStatement(storedStatement);
        return "redirect:/dashboard";
    }

    //Chuyển văn bản từ Văn thư sang chanvanphong
    @PostMapping(path = "/chuyenchanhvanphong")
    public String showChuyenChanhVanPhong(@Valid @ModelAttribute DocumentForward documentForward, Model model) {
        Long currentUserId = commonService.getCurrentUserId();
        documentForward.getReceivedUsers().forEach(userId -> {
            //Log
            DocumentLog documentLog = new DocumentLog();
            documentLog.setCreatedBy(currentUserId);
            documentLog.setDocumentId(documentForward.getDocumentId());

            //Statement
            Statement newStatement = new Statement();
            newStatement.setDocumentId(documentForward.getDocumentId());
            newStatement.setNote(documentForward.getContent());
            newStatement.setUserId(userId);

            User userReceived = userService.findById(userId);

            if (Objects.equals(userId, documentForward.getMainReceivedUser())) {
                documentLog.setStatus("Đã chuyển văn bản đến người xử lý - "+userReceived.getPosition()+"("+userReceived.getName()+")");
                newStatement.setStatus(Status.SENT); //Người xem và có thể xử lý
            } else {
                newStatement.setStatus(Status.RECEIVED); //Người xem văn bản
                documentLog.setStatus("Đã chuyển văn bản đến người xem - "+userReceived.getPosition()+"("+userReceived.getName()+")");
            }
            newStatement.setSenderId(currentUserId);
            statementService.createStatement(newStatement);
            documentLogService.addDocumentLog(documentLog);

        });

        Statement storedStatement = statementService.getStatement(currentUserId, documentForward.getDocumentId());
        storedStatement.setStatus(Status.FORWARDED);
        statementService.updateStatement(storedStatement);
        return "redirect:/dashboard";
    }

    @PostMapping(path = "/chuyenbangiamdoc")
    public String showChuyenBanGiamDoc(@Valid @ModelAttribute DocumentForward documentForward, Model model) {
        log.info(documentForward.toString());
        Long currentUserId = commonService.getCurrentUserId();
        documentForward.getReceivedUsers().forEach(userId -> {
            //Log
            DocumentLog documentLog = new DocumentLog();
            documentLog.setCreatedBy(currentUserId);
            documentLog.setDocumentId(documentForward.getDocumentId());

            Statement newStatement = new Statement();
            newStatement.setDocumentId(documentForward.getDocumentId());
            newStatement.setNote(documentForward.getContent());
            newStatement.setUserId(userId);

            User userReceived = userService.findById(userId);

            if (Objects.equals(userId, documentForward.getMainReceivedUser())) {
                documentLog.setStatus("Đã chuyển văn bản đến người xử lý - "+userReceived.getPosition()+"("+userReceived.getName()+")");
                newStatement.setStatus(Status.SENT);
            } else {
                documentLog.setStatus("Đã chuyển văn bản đến người xem - "+userReceived.getPosition()+"("+userReceived.getName()+")");
                newStatement.setStatus(Status.RECEIVED);
            }
            newStatement.setSenderId(currentUserId);
            documentLogService.addDocumentLog(documentLog);
            statementService.createStatement(newStatement);

        });

        Statement storedStatement = statementService.getStatement(commonService.getCurrentUserId(), documentForward.getDocumentId());
        storedStatement.setStatus(Status.FORWARDED);
        statementService.updateStatement(storedStatement);
        return "redirect:/dashboard";
    }

    @PostMapping(path = "/luuvachuyenchanhvanphong")
    public String showLuuVaChuyenVanBan(@RequestParam(defaultValue = "false") Boolean isLegalDocument,
                                        @RequestParam(defaultValue = "false") Boolean isDirectiveDocument,
                                        @RequestParam(defaultValue = "false") Boolean hasPaperCopy, @Valid @ModelAttribute DocumentForward documentForward,
                                        @ModelAttribute DocumentForm documentForm,
                                        Model model) {
        documentForm.setIsLegalDocument(isLegalDocument);
        documentForm.setIsDirectiveDocument(isDirectiveDocument);
        documentForm.setHasPaperCopy(hasPaperCopy);
        var document = documentService.addNewDocument(documentForm);
        Long currentUserId = commonService.getCurrentUserId();

        documentForward.getReceivedUsers().forEach(userId -> {
            //Log
            DocumentLog documentLog = new DocumentLog();
            documentLog.setCreatedBy(currentUserId);
            documentLog.setDocumentId(documentForward.getDocumentId());

            Statement newStatement = new Statement();
            newStatement.setDocumentId(document.getId());
            newStatement.setNote(documentForward.getContent());
            newStatement.setUserId(userId);

            User userReceived = userService.findById(userId);

            if (Objects.equals(userId, documentForward.getMainReceivedUser())) {
                documentLog.setStatus("Đã chuyển văn bản đến người xử lý - "+userReceived.getPosition()+"("+userReceived.getName()+")");
                newStatement.setStatus(Status.SENT);
            } else {
                documentLog.setStatus("Đã chuyển văn bản đến người xem - "+userReceived.getPosition()+"("+userReceived.getName()+")");
                newStatement.setStatus(Status.RECEIVED);
            }
            newStatement.setSenderId(currentUserId);
            documentLogService.addDocumentLog(documentLog);
            statementService.createStatement(newStatement);

        });

        Statement storedStatement = statementService.getStatement(commonService.getCurrentUserId(), document.getId());
        storedStatement.setStatus(Status.FORWARDED);
        statementService.updateStatement(storedStatement);
        return "redirect:/dashboard";
    }

    //Chuyển văn bản từ Văn thư sang chanvanphong
    @PostMapping(path = "/phancongchuyenvien")
    public String showPhanCongChuyenVien(@Valid @ModelAttribute DocumentForward documentForward, Model model) {
        Long currentUserId = commonService.getCurrentUserId();
        documentForward.getReceivedUsers().forEach(userId -> {
            //Log
            DocumentLog documentLog = new DocumentLog();
            documentLog.setCreatedBy(currentUserId);
            documentLog.setDocumentId(documentForward.getDocumentId());

            //Statement
            Statement newStatement = new Statement();
            newStatement.setDocumentId(documentForward.getDocumentId());
            newStatement.setNote(documentForward.getContent());
            newStatement.setUserId(userId);

            User userReceived = userService.findById(userId);

            documentLog.setStatus("Đã chuyển văn bản đến người xử lý - "+userReceived.getPosition()+"("+userReceived.getName()+")");
            newStatement.setStatus(Status.ASSIGNED); //Người xem và có thể xử lý

            newStatement.setSenderId(currentUserId);
            statementService.createStatement(newStatement);
            documentLogService.addDocumentLog(documentLog);

        });

        Statement storedStatement = statementService.getStatement(currentUserId, documentForward.getDocumentId());
        storedStatement.setStatus(Status.ASSIGNED);
        statementService.updateStatement(storedStatement);
        return "redirect:/dashboard";
    }

    @PostMapping(path="/xulyvanban")
    public String xuLyVanBan(@RequestParam("id") Long documentId){
        Statement storedStatement = statementService.getStatement(commonService.getCurrentUserId(), documentId);
        storedStatement.setStatus(Status.PROCESSED);
        statementService.updateStatement(storedStatement);

        User user = userService.findById(commonService.getCurrentUserId());
        Department department = departmentService.getDepartmentById(user.getDepartmentId());

        DocumentLog documentLog = new DocumentLog();
        documentLog.setDocumentId(documentId);
        documentLog.setCreatedBy(commonService.getCurrentUserId());
        documentLog.setStatus("Đã xử lý văn bản - ("+department.getName()+")");
        documentLogService.addDocumentLog(documentLog);

        return "redirect:/dashboard";
    }
}