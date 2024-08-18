package com.edu.nlu.document.mapper;

import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.payload.DocumentForm;
import org.mapstruct.Mapper;

import java.util.function.Function;

@Mapper
public interface DocumentMapper  {
    Document sourceToDestination(DocumentForm source);

    DocumentForm destinationToSource(Document destination);
}