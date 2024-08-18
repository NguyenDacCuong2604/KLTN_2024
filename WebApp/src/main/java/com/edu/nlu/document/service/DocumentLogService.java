package com.edu.nlu.document.service;

import com.edu.nlu.document.model.DocumentLog;
import com.edu.nlu.document.model.DocumentLogWrapper;

import java.util.List;

public interface DocumentLogService {
    DocumentLog getDocumentLog(int id);
    void addDocumentLog(DocumentLog documentLog);
    List<DocumentLogWrapper> getDocumentLogs(Long idDoc);
}
