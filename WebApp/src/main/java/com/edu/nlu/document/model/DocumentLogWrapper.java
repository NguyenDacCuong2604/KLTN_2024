package com.edu.nlu.document.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DocumentLogWrapper {
    private DocumentLog documentLog;
    private User user;
}
