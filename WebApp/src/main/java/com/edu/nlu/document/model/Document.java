package com.edu.nlu.document.model;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;

@Table(name = "documents")
@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Document {

    @Id
    @GeneratedValue
    private Long id;

    @Column(name = "so_van_ban", nullable = false)
    private String soVanBan;

    @Column(name = "so_den", nullable = false)
    private String soDen;

    @Column(name = "so_ki_hieu_van_ban", nullable = false)
    private String soKiHieuVanBan;

    @Column(name = "co_quan_ban_hanh", nullable = false)
    private String coQuanBanHanh;

    @Column(name = "loai_van_ban", nullable = false)
    private String loaiVanBan;

    @Column(name = "trich_yeu", nullable = false, length = 1000)  // Adjust length as needed
    private String trichYeu;

    @Column(name = "ghi_chu")
    private String ghiChu;

    @Column(name = "van_ban_chi_dao")
    private boolean vanBanChiDao;

    @Column(name = "co_bang_giay")
    private boolean coBangGiay;

    @Column(name = "van_ban_QPPL")
    private boolean vanBanQPPL;

    @Column(name = "ngay_den", nullable = false)
    private LocalDateTime ngayDen;

    @Column(name = "ngay_ban_hanh", nullable = false)
    private LocalDate ngayBanHanh;

    @Column(name = "cap_co_quan")
    private String capCoQuan;

    @Column(name = "linh_vuc")
    private String linhVuc;

    @Column(name = "thoi_gian_xu_ly")
    private LocalDate thoiGianXuLy;

    @Column(name = "thoi_gian_tao")
    private LocalDate thoiGianTao = LocalDate.now();

    @Column(name = "is_delete")
    private boolean isDelete;


//    @Lob
//    @Column(name = "dinh_kem_file")
//    private byte[] dinhKemFile;
}
