package com.edu.nlu.document;

import com.edu.nlu.document.service.DocumentService;
import lombok.RequiredArgsConstructor;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;

@RequiredArgsConstructor
@SpringBootTest
class DocumentApplicationTests {
    @MockBean
    private final DocumentService documentService;


    @Test
    void contextLoads() {
    }


    @Test
    void shouldReturnTrueWhenGetAllDocumentsByUsername() {

    }

}
