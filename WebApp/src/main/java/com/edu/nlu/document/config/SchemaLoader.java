package com.edu.nlu.document.config;

import com.edu.nlu.document.enums.Role;
import com.edu.nlu.document.enums.Status;
import com.edu.nlu.document.model.Department;
import com.edu.nlu.document.model.Document;
import com.edu.nlu.document.model.Statement;
import com.edu.nlu.document.model.User;
import com.edu.nlu.document.repository.DepartmentRepository;
import com.edu.nlu.document.repository.DocumentRepository;
import com.edu.nlu.document.repository.StatementRepository;
import com.edu.nlu.document.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;
import java.util.List;
import java.util.Random;
import java.util.UUID;

@RequiredArgsConstructor
@Configuration
public class SchemaLoader {

    private final UserRepository userRepository;
    private final DocumentRepository documentRepository;
    private final PasswordEncoder passwordEncoder;
    private final StatementRepository statementRepository;
    private final DepartmentRepository departmentRepository;

    @Bean
    CommandLineRunner initDatabase() {
        return args -> {
//            createUsers();
            createDocuments();
            createStatements();
            createUserAndDepartmentRepository();
        };
    }

    private void createUserAndDepartmentRepository() {

        // Department Thanh Tra Sở
        Department department1 = Department.builder()
                .id(1L)
                .name("Thanh Tra Sở")
                .naturalId("2733570")
                .build();

        departmentRepository.save(department1);

        User user8 = User.builder()
                .id(8L)
                .username("nguyenhuuphuoc.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Trưởng phòng")
                .name("Nguyễn Hữu Phước")
                .password(passwordEncoder.encode("password"))
                .departmentId(department1.getId())
                .build();
        department1.setHostId(user8.getId());

        User user9 = User.builder()
                .id(9L)
                .username("nguyenvanbay.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Phó trưởng phòng")
                .name("Nguyễn Văn Bảy")
                .password(passwordEncoder.encode("password"))
                .departmentId(department1.getId())
                .build();

        User user10 = User.builder()
                .id(10L)
                .username("nguyendaclong.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Nhân sự")
                .name("Nguyễn Đắc Long")
                .password(passwordEncoder.encode("password"))
                .departmentId(department1.getId())
                .build();

        // Department Phòng Tổ Chức Biên Chế Và Tổ Chức Phi Chính Phủ
        Department department2 = Department.builder()
                .id(2L)
                .name("Phòng Tổ Chức Biên Chế Và Tổ Chức Phi Chính Phủ")
                .naturalId("2733552")
                .build();

        departmentRepository.save(department2);

        User user11 = User.builder()
                .id(11L)
                .username("duongduymen.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Trưởng phòng")
                .name("Dương Duy Mến")
                .password(passwordEncoder.encode("password"))
                .departmentId(department2.getId())
                .build();
        department2.setHostId(user11.getId());

        User user12 = User.builder()
                .id(12L)
                .username("nguyenvanbe.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Phó trưởng phòng")
                .name("Nguyễn Văn Be")
                .password(passwordEncoder.encode("password"))
                .departmentId(department2.getId())
                .build();

        User user13 = User.builder()
                .id(13L)
                .username("nguyendacsinh.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Nhân sự")
                .name("Nguyễn Đắc Sinh")
                .password(passwordEncoder.encode("password"))
                .departmentId(department2.getId())
                .build();

        // Department Phòng Công Chức Viên Chức
        Department department3 = Department.builder()
                .id(3L)
                .name("Phòng Công Chức Viên Chức")
                .naturalId("2733546")
                .build();

        departmentRepository.save(department3);

        User user14 = User.builder()
                .id(14L)
                .username("nguyenthia.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Trưởng phòng")
                .name("Nguyễn Thị A")
                .password(passwordEncoder.encode("password"))
                .departmentId(department3.getId())
                .build();
        department3.setHostId(user14.getId());

        User user15 = User.builder()
                .id(15L)
                .username("nguyenthib.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Phó trưởng phòng")
                .name("Nguyễn Thị B")
                .password(passwordEncoder.encode("password"))
                .departmentId(department3.getId())
                .build();

        User user16 = User.builder()
                .id(16L)
                .username("nguyenthic.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Nhân sự")
                .name("Nguyễn Thị C")
                .password(passwordEncoder.encode("password"))
                .departmentId(department3.getId())
                .build();

        // Department Ban Thi Đua Khen Thưởng
        Department department4 = Department.builder()
                .id(4L)
                .name("Ban Thi Đua Khen Thưởng")
                .naturalId("2733522")
                .build();

        departmentRepository.save(department4);

        User user17 = User.builder()
                .id(17L)
                .username("tranthia.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Trưởng phòng")
                .name("Trần Thị A")
                .password(passwordEncoder.encode("password"))
                .departmentId(department4.getId())
                .build();
        department4.setHostId(user17.getId());

        User user18 = User.builder()
                .id(18L)
                .username("tranthib.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Phó trưởng phòng")
                .name("Trần Thị B")
                .password(passwordEncoder.encode("password"))
                .departmentId(department4.getId())
                .build();

        User user19 = User.builder()
                .id(19L)
                .username("tranthic.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Nhân sự")
                .name("Trần Thị C")
                .password(passwordEncoder.encode("password"))
                .departmentId(department4.getId())
                .build();

        // Department Chi Cục Văn Thư Lưu Trữ
        Department department5 = Department.builder()
                .id(5L)
                .name("Chi Cục Văn Thư Lưu Trữ")
                .naturalId("2733534")
                .build();

        departmentRepository.save(department5);

        User user20 = User.builder()
                .id(20L)
                .username("lethia.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Trưởng phòng")
                .name("Lê Thị A")
                .password(passwordEncoder.encode("password"))
                .departmentId(department5.getId())
                .build();
        department5.setHostId(user20.getId());

        User user21 = User.builder()
                .id(21L)
                .username("lethib.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Phó trưởng phòng")
                .name("Lê Thị B")
                .password(passwordEncoder.encode("password"))
                .departmentId(department5.getId())
                .build();

        User user22 = User.builder()
                .id(22L)
                .username("lethic.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Nhân sự")
                .name("Lê Thị C")
                .password(passwordEncoder.encode("password"))
                .departmentId(department5.getId())
                .build();

        // Department Phòng Cải Cách Hành Chính
        Department department6 = Department.builder()
                .id(6L)
                .name("Phòng Cải Cách Hành Chính")
                .naturalId("2733540")
                .build();

        departmentRepository.save(department6);

        User user23 = User.builder()
                .id(23L)
                .username("hoangthithao.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Trưởng phòng")
                .name("Hoàng Thị Thảo")
                .password(passwordEncoder.encode("password"))
                .departmentId(department6.getId())
                .build();
        department6.setHostId(user23.getId());

        User user24 = User.builder()
                .id(24L)
                .username("hoangthib.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Phó trưởng phòng")
                .name("Hoàng Thị B")
                .password(passwordEncoder.encode("password"))
                .departmentId(department6.getId())
                .build();

        User user25 = User.builder()
                .id(25L)
                .username("hoangthic.snv")
                .role(String.valueOf(Role.CHUYEN_VIEN))
                .position("Nhân sự")
                .name("Hoàng Thị C")
                .password(passwordEncoder.encode("password"))
                .departmentId(department6.getId())
                .build();

        // Department Quản lý
        Department department7 = Department.builder()
                .id(7L)
                .name("Quản lý")
                .naturalId("0000000")
                .build();

        departmentRepository.save(department7);

        User user1 = User.builder()
                .username("vanthu.snv")
                .role(String.valueOf(Role.VAN_THU))
                .position("Văn thư")
                .password(passwordEncoder.encode("password"))
                .name("Văn thư")
                .departmentId(department7.getId())
                .build();

        User user2 = User.builder()
                .username("chanhvanphong.snv")
                .role(String.valueOf(Role.CHANH_VAN_PHONG))
                .position("Chánh Văn Phòng")
                .password(passwordEncoder.encode("password"))
                .name("Chánh Văn Phòng")
                .departmentId(department7.getId())
                .build();

        User user3 = User.builder()
                .username("lemongtrang.svn")
                .role(String.valueOf(Role.CHANH_VAN_PHONG))
                .position("Chuyên viên")
                .password(passwordEncoder.encode("password"))
                .name("Lê Mộng Trang")
                .departmentId(department7.getId())
                .build();

        User user4 = User.builder()
                .username("huynhthanhnhan.snv")
                .role(String.valueOf(Role.BAN_GIAM_DOC))
                .position("Giám đốc")
                .password(passwordEncoder.encode("password"))
                .name("Huỳnh Thanh Nhân")
                .departmentId(department7.getId())
                .build();

        User user5 = User.builder()
                .username("nguyenbacnam.snv")
                .role(String.valueOf(Role.BAN_GIAM_DOC))
                .position("Phó Giám Đốc")
                .password(passwordEncoder.encode("password"))
                .name("Nguyễn Bắc Nam")
                .departmentId(department7.getId())
                .build();

        User user6 = User.builder()
                .username("phankieuthanhhuong.snv")
                .role(String.valueOf(Role.BAN_GIAM_DOC))
                .position("Phó Giám Đốc")
                .password(passwordEncoder.encode("password"))
                .name("Phan Kiều Thanh Hương")
                .departmentId(department7.getId())
                .build();

        User user7 = User.builder()
                .username("nguyenthihongtham.snv")
                .role(String.valueOf(Role.BAN_GIAM_DOC))
                .position("Phó Giám Đốc")
                .password(passwordEncoder.encode("password"))
                .name("Nguyễn Thị Hồng Thắm")
                .departmentId(department7.getId())
                .build();

        // Lưu tất cả User
        userRepository.saveAll(List.of(
                user1, user2, user3, user4, user5, user6, user7, user8, user9, user10,
                user11, user12, user13, user14, user15, user16, user17, user18, user19,
                user20, user21, user22, user23, user24, user25
        ));

        // Lưu tất cả các thay đổi của Department
        departmentRepository.saveAll(List.of(
                department1, department2, department3, department4, department5, department6, department7
        ));
    }

    private void createDocuments() {
        Document doc1 = Document.builder()
                .id(1L)
                .soVanBan("1002/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("01/KH-UBND")
                .coQuanBanHanh("Ủy ban nhân dân Quận 3 TP.HCM")
                .loaiVanBan("Kế hoạch")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.now())
                .trichYeu("Tổ chức Hội nghị triển khai nhiệm vụ phát triển kinh tế xã hội năm 2022 chủ đề Thích ứng an toàn, linh hoạt kiểm soát hiệu quả dịch covid-19, tiếp tục nâng cao chất lượng xây dựng đô thị, cải thiện môi trường đầu tư đẩy mạnh cải cách hành chính và đồng hành cùng doanh nghiệp")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Kinh tế")
                .ghiChu("Xử lý gấp")
                .build();

        Document doc2 = Document.builder()
                .id(2L)
                .soVanBan("1003/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("02/BC-BDT")
                .coQuanBanHanh("Ban Dân tộc - TPHCM")
                .loaiVanBan("Báo cáo")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.of(2022, 6, 1))
                .trichYeu("Báo cáo sơ kết 01 năm thực hiện Chương trình cải cách hành chính và giải pháp nâng cao Chỉ số cải cách hành chính giai đoạn 2020-2025 tại Ban Dân tộc Thành phố")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Cải cách hành chính")
                .ghiChu("Xử lý gấp")
                .build();

        Document doc3 = Document.builder()
                .id(3L)
                .soVanBan("1004/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("02/BC-SNN")
                .coQuanBanHanh("Sở Nông nghiệp và Phát triển nông thôn TP.HCM")
                .loaiVanBan("Báo cáo")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.of(2022, 5, 1))
                .trichYeu("Báo cáo sơ kết 01 năm thực hiện Chương trình cải cách hành chính (viết tắt là CCHC) và giải pháp nâng cao Chỉ số cải cách hành chính trên địa bàn Thành phố giai đoạn 2020 - 2025")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Cải cách hành chính")
                .ghiChu("Xử lý gấp")
                .build();

        Document doc4 = Document.builder()
                .id(4L)
                .soVanBan("1005/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("02/BC-TTTP")
                .coQuanBanHanh("Thanh tra Thành phố - TPHCM")
                .loaiVanBan("Báo cáo")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.of(2022, 7, 1))
                .trichYeu("Báo cáo sơ kết 01 năm thực hiện Chương trình cải cách hành chính và giải pháp nâng cao chỉ số cải cách hành chính giai đoạn 2020-2025 tại Thanh tra Thành phố")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Cải cách hành chính")
                .ghiChu("Xử lý gấp")
                .build();

        Document doc5 = Document.builder()
                .id(5L)
                .soVanBan("1006/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("02/BC-UBND")
                .coQuanBanHanh("Ủy ban nhân dân Quận Phú Nhuận TP.HCM")
                .loaiVanBan("Báo cáo")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.of(2022, 7, 6))
                .trichYeu("Báo cáo kết quả công tác CCHC trên địa bàn quận Phú Nhuận giai đoạn 2020-2025")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Cải cách hành chính")
                .ghiChu("Xử lý gấp")
                .build();

        Document doc6 = Document.builder()
                .id(6L)
                .soVanBan("1007/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("02/CT-UBND")
                .coQuanBanHanh("Ủy ban nhân dân Quận Tân Phú TP.HCM")
                .loaiVanBan("Chỉ thị")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.of(2022, 5, 31))
                .trichYeu("V/v lập danh sách điều tra xã hội học phục vụ xác định Chỉ số Cải cách hành chính năm 2021 của Thành phố")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Cải cách hành chính")
                .ghiChu("Xử lý gấp")
                .build();

        Document doc7 = Document.builder()
                .id(7L)
                .soVanBan("1008/SNV")
                .soDen("HSK")
                .soKiHieuVanBan("02/UBND")
                .coQuanBanHanh("Ủy ban nhân dân Quận Phú Nhuận TP.HCM")
                .loaiVanBan("Công văn")
                .ngayDen(LocalDateTime.now())
                .ngayBanHanh(LocalDate.of(2022, 5, 1))
                .trichYeu("V/v điều tra xã hội học phục vụ xác định Chỉ số Cải cách hành chính năm 2021 của Thành phố")
                .coBangGiay(true)
                .thoiGianTao(LocalDate.now())
                .thoiGianXuLy(LocalDate.now())
                .vanBanChiDao(true)
                .vanBanQPPL(true)
                .capCoQuan("Cơ quan xử lý")
                .linhVuc("Cải cách hành chính")
                .ghiChu("Xử lý gấp")
                .build();


        documentRepository.saveAll(List.of(doc1,doc2,doc3,doc4,doc5,doc6, doc7));

    }


    void createUsers() {

        // Create and persist Users
        User user1 = new User();
        user1.setUsername("user1");
        user1.setRole(Role.VAN_THU);
        user1.setPosition("Văn thư");
        user1.setPassword(passwordEncoder.encode("password"));
        user1.setName("Văn thư");

        User user2 = new User();
        user2.setUsername("user2");
        user2.setRole(Role.CHANH_VAN_PHONG);
        user2.setPosition("Chánh Văn Phòng");
        user2.setPassword(passwordEncoder.encode("password"));
        user2.setName("Chánh Văn Phòng");

        User user3 = new User();
        user3.setUsername("user3");
        user3.setRole(Role.CHANH_VAN_PHONG);
        user3.setPosition("Chuyên viên");
        user3.setPassword(passwordEncoder.encode("password"));
        user3.setName("Lê Mộng Trang");

        User user4 = new User();
        user4.setUsername("user4");
        user4.setRole(Role.BAN_GIAM_DOC);
        user4.setPosition("Giám đốc");
        user4.setPassword(passwordEncoder.encode("password"));
        user4.setName("Huỳnh Thanh Nhân");

        User user5 = new User();
        user5.setUsername("user5");
        user5.setRole(Role.BAN_GIAM_DOC);
        user5.setPosition("Phó Giám Đốc");
        user5.setPassword(passwordEncoder.encode("password"));
        user5.setName("Nguyễn Bắc Nam");

        User user6 = new User();
        user6.setUsername("user6");
        user6.setRole(Role.BAN_GIAM_DOC);
        user6.setPosition("Phó Giám Đốc");
        user6.setPassword(passwordEncoder.encode("password"));
        user6.setName("Phan Kiều Thanh Hương");

        User user7 = new User();
        user7.setUsername("user7");
        user7.setRole(Role.BAN_GIAM_DOC);
        user7.setPosition("Phó Giám Đốc");
        user7.setPassword(passwordEncoder.encode("password"));
        user7.setName("Nguyễn Thị Hồng Thắm");

        userRepository.save(user1);
        userRepository.save(user2);
        userRepository.save(user3);
        userRepository.save(user4);
        userRepository.save(user5);
        userRepository.save(user6);
        userRepository.save(user7);
    }

    void createStatements(){
        Statement statement1 = new Statement();
        statement1.setId(1L);
        statement1.setStatus(Status.CREATED);
        statement1.setUserId(1L);
        statement1.setDocumentId(1L);
        statement1.setSenderId(1L);

        Statement statement2 = new Statement();
        statement2.setId(2L);
        statement2.setStatus(Status.CREATED);
        statement2.setUserId(1L);
        statement2.setDocumentId(2L);
        statement2.setSenderId(1L);

        Statement statement3 = new Statement();
        statement3.setId(3L);
        statement3.setStatus(Status.CREATED);
        statement3.setUserId(1L);
        statement3.setDocumentId(3L);
        statement3.setSenderId(1L);

        Statement statement4 = new Statement();
        statement4.setId(4L);
        statement4.setStatus(Status.CREATED);
        statement4.setUserId(1L);
        statement4.setDocumentId(4L);
        statement4.setSenderId(1L);

        Statement statement5 = new Statement();
        statement5.setId(5L);
        statement5.setStatus(Status.CREATED);
        statement5.setUserId(1L);
        statement5.setDocumentId(5L);
        statement5.setSenderId(1L);

        Statement statement6 = new Statement();
        statement6.setId(6L);
        statement6.setStatus(Status.CREATED);
        statement6.setUserId(1L);
        statement6.setDocumentId(6L);
        statement6.setSenderId(1L);

        Statement statement7 = new Statement();
        statement7.setId(7L);
        statement7.setStatus(Status.CREATED);
        statement7.setUserId(1L);
        statement7.setDocumentId(7L);
        statement7.setSenderId(1L);

        Statement statement8 = new Statement();
        statement8.setId(1L);
        statement8.setStatus(Status.FORWARDED);
        statement8.setUserId(1L);
        statement8.setDocumentId(1L);
        statement8.setSenderId(1L);

        Statement statement9 = new Statement();
        statement9.setId(8L);
        statement9.setStatus(Status.SENT);
        statement9.setUserId(2L);
        statement9.setDocumentId(1L);
        statement9.setSenderId(1L);

        Statement statement10 = new Statement();
        statement10.setId(9L);
        statement10.setStatus(Status.RECEIVED);
        statement10.setUserId(3L);
        statement10.setDocumentId(1L);
        statement10.setSenderId(1L);

        statementRepository.save(statement1);
        statementRepository.save(statement2);
        statementRepository.save(statement3);
        statementRepository.save(statement4);
        statementRepository.save(statement5);
        statementRepository.save(statement6);
        statementRepository.save(statement7);
        statementRepository.save(statement8);
        statementRepository.save(statement9);
        statementRepository.save(statement10);
    }
}
