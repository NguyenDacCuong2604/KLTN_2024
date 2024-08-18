package com.edu.nlu.document.service;

import com.edu.nlu.document.model.Statement;

import java.util.List;

public interface StatementService {

    void createStatement(Statement statement);

    void updateStatement(Statement statement);

    Statement getStatement(Long userId, Long documentId);

    List<Statement> getStatementsByCurrentUser();

}
