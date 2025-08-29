-- 작업자 테이블 생성
CREATE TABLE IF NOT EXISTS workers (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    position VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    image VARCHAR(500)
);

-- 근무 날짜 테이블 생성
CREATE TABLE IF NOT EXISTS working_dates (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    worker_id BIGINT NOT NULL,
    work_date DATE NOT NULL,
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE
);

-- 샘플 데이터 삽입
INSERT INTO workers (employee_id, name, position, phone, image) VALUES
('201902927', 'Sarah Johnson', 'Safety Inspector', '+1(555) 987-6543', NULL),
('202011234', 'Daniel Kim', 'Safety Inspector', '+1(555) 987-6543', NULL);

-- 샘플 근무 날짜 데이터 삽입
INSERT INTO working_dates (worker_id, work_date) VALUES
(1, '2025-08-22'),
(1, '2025-08-23'),
(1, '2025-08-25'),
(2, '2025-09-01'),
(2, '2025-09-02');
