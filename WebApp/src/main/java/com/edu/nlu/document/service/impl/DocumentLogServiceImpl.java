package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.model.DocumentLog;
import com.edu.nlu.document.model.DocumentLogWrapper;
import com.edu.nlu.document.model.User;
import com.edu.nlu.document.repository.DocumentLogRepository;
import com.edu.nlu.document.service.DocumentLogService;
import com.edu.nlu.document.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class DocumentLogServiceImpl implements DocumentLogService {
    private final DocumentLogRepository documentLogRepository;
    private final UserService userService;

    @Override
    public DocumentLog getDocumentLog(int id) {
        return null;
    }

    @Override
    public void addDocumentLog(DocumentLog documentLog) {
        documentLogRepository.save(documentLog);
    }

    @Override
    public List<DocumentLogWrapper> getDocumentLogs(Long idDoc) {
        List<DocumentLogWrapper> documentLogsWrapper = new ArrayList<>();
        List<DocumentLog> documentLogs = documentLogRepository.findDocumentLogsByDocumentIdOrderByCreatedDateAsc(idDoc);
        for (DocumentLog documentLog : documentLogs) {
            DocumentLogWrapper documentLogWrapper = new DocumentLogWrapper();
            documentLogWrapper.setDocumentLog(documentLog);
            documentLogWrapper.setUser(userService.findById(documentLog.getCreatedBy()));
            documentLogsWrapper.add(documentLogWrapper);
        }
        return documentLogsWrapper;
    }
}
