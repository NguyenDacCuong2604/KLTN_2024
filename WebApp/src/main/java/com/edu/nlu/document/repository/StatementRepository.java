package com.edu.nlu.document.repository;

import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.model.Statement;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StatementRepository extends JpaRepository<Statement, Long> {

    Optional<Statement> findByUserIdAndDocumentId(Long userId, Long documentId);

    @Query("SELECT s FROM Document d JOIN Statement s ON d.id = s.documentId WHERE s.userId = :userId AND d.isDelete != true ORDER BY d.ngayDen DESC")
    List<Statement> findAllStatementsByUserId(@Param("userId") Long userId);
}
