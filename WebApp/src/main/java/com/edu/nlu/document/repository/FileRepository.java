package com.edu.nlu.document.repository;

import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.model.File;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FileRepository extends JpaRepository<File, Long> {

    List<File> findAllByDocumentId(Long documentId);

}
