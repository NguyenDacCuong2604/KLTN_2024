package com.edu.nlu.document.payload;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Builder
@ToString
@Getter
@Setter
public class DocumentForward {
    Long documentId;

    List<Long> receivedUsers;

    String content;

    Long mainReceivedUser;

}
