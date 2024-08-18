package com.edu.nlu.document.model;

import com.edu.nlu.document.enums.Status;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDateTime;

@Table(name = "document_logs")
@Entity
@Getter
@Setter
public class DocumentLog {

    @Id
    @GeneratedValue
    private Long id;

    private String status;

    private Long createdBy;

    private LocalDateTime createdDate = LocalDateTime.now();

    private Long documentId;


}
