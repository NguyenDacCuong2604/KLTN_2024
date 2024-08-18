package com.edu.nlu.document.service;

import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.payload.DocumentForm;

import java.util.List;

public interface DocumentService {

    List<Document> getAllDocumentsByCurrentUser();

    Document addNewDocument(DocumentForm documentForm);

    Document getDocumentById(Long id);
    void deleteDocument(Long documentId);
}
