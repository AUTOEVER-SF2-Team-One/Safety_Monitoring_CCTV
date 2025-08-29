package com.autoever.controller;

import com.autoever.model.WorkerModel;
import com.autoever.model.ErrorResponse;
import com.autoever.service.WorkerService;
import com.autoever.util.ValidationUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/workers")
@CrossOrigin(origins = "http://localhost:5173")
public class WorkerController {
    private final WorkerService workerService;

    @Autowired
    public WorkerController(WorkerService workerService) {
        this.workerService = workerService;
    }

    // 모든 작업자 조회
    @GetMapping
    public ResponseEntity<?> getAllWorkers() {
        try {
            List<WorkerModel> workers = workerService.getAllWorkers();
            return ResponseEntity.ok(workers);
        } catch (Exception e) {
            ErrorResponse error = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Internal Server Error",
                "서버 내부 오류가 발생했습니다.",
                e.getMessage()
            );
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    // 특정 작업자 조회
    @GetMapping("/{id}")
    public ResponseEntity<?> getWorkerById(@PathVariable Long id) {
        try {
            WorkerModel worker = workerService.getWorkerById(id);
            if (worker == null) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.NOT_FOUND.value(),
                    "Not Found",
                    "요청한 작업자를 찾을 수 없습니다.",
                    "ID: " + id + "인 작업자가 존재하지 않습니다."
                );
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
            }
            return ResponseEntity.ok(worker);
        } catch (Exception e) {
            ErrorResponse error = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Internal Server Error",
                "서버 내부 오류가 발생했습니다.",
                e.getMessage()
            );
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    // 새로운 작업자 추가
    @PostMapping
    public ResponseEntity<?> createWorker(@RequestBody WorkerModel worker) {
        try {
            // ValidationUtil을 사용한 유효성 검사
            ValidationUtil.ValidationResult validationResult = ValidationUtil.validateWorker(worker);
            if (!validationResult.isValid()) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.BAD_REQUEST.value(),
                    "Bad Request",
                    "입력 데이터가 유효하지 않습니다.",
                    String.join(", ", validationResult.getErrors())
                );
                return ResponseEntity.badRequest().body(error);
            }

            // 사원번호 중복 체크
            if (workerService.existsByEmployeeId(worker.getEmployeeId())) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.CONFLICT.value(),
                    "Conflict",
                    "이미 존재하는 사원번호입니다.",
                    "사원번호 " + worker.getEmployeeId() + "는 이미 등록되어 있습니다."
                );
                return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
            }

            WorkerModel createdWorker = workerService.createWorker(worker);
            return ResponseEntity.status(HttpStatus.CREATED).body(createdWorker);
        } catch (RuntimeException e) {
            if (e.getMessage().contains("이미 존재하는 사원번호")) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.CONFLICT.value(),
                    "Conflict",
                    "이미 존재하는 사원번호입니다.",
                    e.getMessage()
                );
                return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
            }
            ErrorResponse error = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                "Bad Request",
                "입력 데이터가 유효하지 않습니다.",
                e.getMessage()
            );
            return ResponseEntity.badRequest().body(error);
        } catch (Exception e) {
            ErrorResponse error = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Internal Server Error",
                "서버 내부 오류가 발생했습니다.",
                e.getMessage()
            );
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    // 작업자 정보 수정
    @PutMapping("/{id}")
    public ResponseEntity<?> updateWorker(@PathVariable Long id, @RequestBody WorkerModel worker) {
        try {
            // ValidationUtil을 사용한 유효성 검사
            ValidationUtil.ValidationResult validationResult = ValidationUtil.validateWorker(worker);
            if (!validationResult.isValid()) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.BAD_REQUEST.value(),
                    "Bad Request",
                    "입력 데이터가 유효하지 않습니다.",
                    String.join(", ", validationResult.getErrors())
                );
                return ResponseEntity.badRequest().body(error);
            }

            WorkerModel updatedWorker = workerService.updateWorker(id, worker);
            return ResponseEntity.ok(updatedWorker);
        } catch (RuntimeException e) {
            if (e.getMessage().contains("찾을 수 없습니다")) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.NOT_FOUND.value(),
                    "Not Found",
                    "수정할 작업자를 찾을 수 없습니다.",
                    e.getMessage()
                );
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
            }
            ErrorResponse error = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                "Bad Request",
                "입력 데이터가 유효하지 않습니다.",
                e.getMessage()
            );
            return ResponseEntity.badRequest().body(error);
        } catch (Exception e) {
            ErrorResponse error = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Internal Server Error",
                "서버 내부 오류가 발생했습니다.",
                e.getMessage()
            );
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    // 작업자 삭제
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteWorker(@PathVariable Long id) {
        try {
            boolean deleted = workerService.deleteWorker(id);
            if (deleted) {
                return ResponseEntity.noContent().build();
            } else {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.INTERNAL_SERVER_ERROR.value(),
                    "Internal Server Error",
                    "작업자 삭제에 실패했습니다.",
                    "알 수 없는 오류가 발생했습니다."
                );
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
            }
        } catch (RuntimeException e) {
            if (e.getMessage().contains("찾을 수 없습니다")) {
                ErrorResponse error = new ErrorResponse(
                    HttpStatus.NOT_FOUND.value(),
                    "Not Found",
                    "삭제할 작업자를 찾을 수 없습니다.",
                    e.getMessage()
                );
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
            }
            ErrorResponse error = new ErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                "Bad Request",
                "삭제 요청이 유효하지 않습니다.",
                e.getMessage()
            );
            return ResponseEntity.badRequest().body(error);
        } catch (Exception e) {
            ErrorResponse error = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "Internal Server Error",
                "서버 내부 오류가 발생했습니다.",
                e.getMessage()
            );
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}
