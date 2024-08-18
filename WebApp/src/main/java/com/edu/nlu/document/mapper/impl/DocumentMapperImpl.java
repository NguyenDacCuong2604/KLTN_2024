package com.edu.nlu.document.mapper.impl;

import com.edu.nlu.document.mapper.DocumentMapper;
import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.payload.DocumentForm;
import org.springframework.stereotype.Component;

import java.time.LocalDate;

@Component
public class DocumentMapperImpl implements DocumentMapper {
    @Override
    public Document sourceToDestination(DocumentForm source) {
        if (source == null) {
            return null;
        }
        return Document.builder()
                .soVanBan(source.getDocumentNumber())
                .trichYeu(source.getSummary())
                .capCoQuan(source.getAgencyLevel())
                .coQuanBanHanh(source.getIssuingAgency())
                .ghiChu(source.getNote())
                .soDen(source.getArrivalNumber())
                .linhVuc(source.getField())
                .loaiVanBan(source.getDocumentType())
                .ngayDen(source.getArrivalDate())
                .ngayBanHanh(source.getIssueDate())
                .soKiHieuVanBan(source.getDocumentSymbol())
                .thoiGianXuLy(source.getProcessingTime())
                .coBangGiay(source.getHasPaperCopy())
                .vanBanQPPL(source.getIsLegalDocument())
                .vanBanChiDao(source.getIsDirectiveDocument())
                .thoiGianTao(LocalDate.now())
                .build();
    }

    @Override
    public DocumentForm destinationToSource(Document destination) {
        if (destination == null) {
            return null;
        }

        return DocumentForm.builder()
                .documentNumber(destination.getSoVanBan())
                .summary(destination.getTrichYeu())
                .agencyLevel(destination.getCapCoQuan())
                .hasPaperCopy(destination.isCoBangGiay())
                .issuingAgency(destination.getCoQuanBanHanh())
                .note(destination.getGhiChu())
                .arrivalNumber(destination.getSoDen())
                .field(destination.getLinhVuc())
                .documentType(destination.getLoaiVanBan())
                .issueDate(destination.getThoiGianTao())
                .documentSymbol(destination.getSoKiHieuVanBan())
                .processingTime(destination.getThoiGianXuLy())
                .isLegalDocument(destination.isVanBanQPPL())
                .isDirectiveDocument(destination.isVanBanChiDao())
                .hasPaperCopy(destination.isCoBangGiay())
                .arrivalDate(destination.getNgayDen())
                .build();
    }
}
