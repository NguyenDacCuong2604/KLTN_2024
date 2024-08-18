package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.model.File;
import com.edu.nlu.document.repository.FileRepository;
import com.edu.nlu.document.service.FileService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@RequiredArgsConstructor
@Service
public class FileServiceImpl implements FileService {
    private final FileRepository fileRepository;

    @Override
    public List<File> getAllFileByDocumentId(Long documentId) {
        return fileRepository.findAllByDocumentId(documentId);
    }

    @Override
    public void saveAll(List<File> files) {
        fileRepository.saveAll(files);
    }
}
