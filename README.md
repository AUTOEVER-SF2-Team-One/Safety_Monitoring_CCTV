# Safete_Monitoring_CCTV
현대오토에버 모빌리티 스쿨 스마트팩토리 2기 머신비전 프로젝트

## Model Files

모델파일이 너무 커서 github에 올라가지 않습니다. 때문에 아래 링크로 직접 다운로드 받으시거나 아래 방법을 사용하십시오

`./body/ 경로로 저장`
https://drive.google.com/file/d/1-ZvAT3zgfrk2lHSAzikznbus-6E6iBhz/view?usp=drive_link
https://drive.google.com/file/d/1jF5Yf-l3yqELDPcbg-Uu9Se93rlaJL3p/view?usp=drive_link
https://drive.google.com/file/d/1BOenTL_Kj4VAkb7F-39n82L_YqcJZ01T/view?usp=sharing


First, you need to install `gdown`:
```bash
pip install gdown
```

Then, you can download the model files using the following commands:

**hat_model_cap.pt**
```bash
gdown --id 1-ZvAT3zgfrk2lHSAzikznbus-6E6iBhz -O body/hat_model_cap.pt
```

**hat_model_v1.pt**
```bash
gdown --id 1jF5Yf-l3yqELDPcbg-Uu9Se93rlaJL3p -O body/hat_model_v1.pt
```

**person_model_yolov8m.pt**
```bash
gdown --id 1BOenTL_Kj4VAkb7F-39n82L_YqcJZ01T -O body/person_model_yolov8m.pt
```