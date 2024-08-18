package com.edu.nlu.document.service;

import com.edu.nlu.document.model.File;

import java.util.List;

public interface FileService {
    List<File> getAllFileByDocumentId(Long documentId);

    void saveAll(List<File> files);
}
