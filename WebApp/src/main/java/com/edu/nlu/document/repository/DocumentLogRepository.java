package com.edu.nlu.document.repository;

import com.edu.nlu.document.model.DocumentLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface DocumentLogRepository extends JpaRepository<DocumentLog, Long> {
    List<DocumentLog> findDocumentLogsByDocumentIdOrderByCreatedDateAsc(Long id);
}
