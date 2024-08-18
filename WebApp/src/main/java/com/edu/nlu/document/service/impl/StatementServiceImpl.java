package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.model.Statement;
import com.edu.nlu.document.repository.StatementRepository;
import com.edu.nlu.document.service.CommonService;
import com.edu.nlu.document.service.StatementService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@RequiredArgsConstructor
@Service
public class StatementServiceImpl implements StatementService {

    private final StatementRepository statementRepository;
    private final CommonService commonService;


    @Override
    public void createStatement(Statement statement) {
        statementRepository.save(statement);
    }

    @Override
    public void updateStatement(Statement statement) {
        statementRepository.save(statement);
    }

    @Override
    public Statement getStatement(Long userId, Long documentId) {
        return statementRepository.findByUserIdAndDocumentId(userId, documentId).orElseThrow(() -> new IllegalArgumentException("Statement not found"));
    }

    @Override
    public List<Statement> getStatementsByCurrentUser() {
        return statementRepository.findAllStatementsByUserId(commonService.getCurrentUserId());
    }
}
