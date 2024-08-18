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
public class DocumentForm {

    @NotEmpty(message = "Số văn bản is required")
    private String documentNumber;

    private Boolean isLegalDocument;

    @NotEmpty(message = "Số đến is required")
    private String arrivalNumber;

    @NotNull(message = "Ngày đến is required")
    private LocalDateTime arrivalDate;

    @NotEmpty(message = "Số ký hiệu của văn bản is required")
    private String documentSymbol;

    @NotNull(message = "Ngày ban hành is required")
    private LocalDate issueDate;

    @NotEmpty(message = "Cơ quan ban hành is required")
    private String issuingAgency;

    private String agencyLevel;

    private String documentType;

    private String field;

    @NotEmpty(message = "Trích yếu is required")
    private String summary;

    private String note;

    private Boolean isDirectiveDocument;

    private LocalDate processingTime;

    private Boolean hasPaperCopy;

    private List<MultipartFile> attachedFiles;
}
