package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.enums.Status;
import com.edu.nlu.document.mapper.DocumentMapper;
import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.model.DocumentLog;
import com.edu.nlu.document.model.File;
import com.edu.nlu.document.model.Statement;
import com.edu.nlu.document.payload.DocumentForm;
import com.edu.nlu.document.repository.DocumentRepository;
import com.edu.nlu.document.service.*;
import com.edu.nlu.document.util.FileUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Objects;

@Service
@RequiredArgsConstructor
public class DocumentServiceImpl implements DocumentService {
    private final DocumentRepository documentRepository;
    private final DocumentMapper documentMapper;
    private final FileService fileService;
    private final StatementService statementService;
    private final CommonService commonService;
    private final DocumentLogService documentLogService;

    @Override
    public List<Document> getAllDocumentsByCurrentUser() {
        Long userId = commonService.getCurrentUserId();
        return documentRepository.findAllDocumentsByUserId(userId);
    }

    @Override
    public Document addNewDocument(DocumentForm documentForm) {
        var storedDocument = documentRepository.save(documentMapper.sourceToDestination(documentForm));
        List<MultipartFile> files = documentForm.getAttachedFiles();
        List<File> list = files.stream()
                .filter(multipartFile -> multipartFile.getSize() > 0) // Lọc những file có size > 0
                .map(multipartFile -> File.builder()
                        .name(multipartFile.getOriginalFilename())
                        .path("/assets/files/" + multipartFile.getOriginalFilename())
                        .size(multipartFile.getSize())
                        .documentId(storedDocument.getId())
                        .extension(FileUtil.getExtension(Objects.requireNonNull(multipartFile.getOriginalFilename())))
                        .build())
                .toList();
        fileService.saveAll(list);

        //Statement
        Statement newStatement = new Statement();
        newStatement.setDocumentId(storedDocument.getId());
        newStatement.setUserId(commonService.getCurrentUserId());
        newStatement.setSenderId(commonService.getCurrentUserId());
        newStatement.setStatus(Status.CREATED);
        statementService.createStatement(newStatement);

        //Log
        DocumentLog documentLog = new DocumentLog();
        documentLog.setDocumentId(storedDocument.getId());
        documentLog.setCreatedBy(commonService.getCurrentUserId());
        documentLog.setStatus("Đã tạo 1 văn bản đến");
        documentLogService.addDocumentLog(documentLog);

        return storedDocument;
    }

    @Override
    public Document getDocumentById(Long id) {
        return documentRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Document not found"));
    }

    @Override
    public void deleteDocument(Long documentId) {
        Document document = documentRepository.findById(documentId).orElseThrow(() -> new IllegalArgumentException("Document not found"));
        document.setDelete(true);
        documentRepository.save(document);
    }
}
