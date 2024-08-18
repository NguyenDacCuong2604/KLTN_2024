package com.edu.nlu.document.model;

import com.edu.nlu.document.enums.Status;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@AllArgsConstructor
@NoArgsConstructor
@Table(name = "statements")
@Entity
@Data
public class Statement {
    @Id
    @GeneratedValue
    private Long id;

    private Long documentId;

    private String note;

    private Long userId;

    private Long senderId;

    @Enumerated(EnumType.STRING)
    private Status status;
}
