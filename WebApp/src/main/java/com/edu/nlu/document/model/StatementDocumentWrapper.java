package com.edu.nlu.document.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class StatementDocumentWrapper {
    private Document document;
    private Statement statement;
    private User userSender;
}
