script to run env
cd ../current_ml/model1/model/scripts && activate && cd ../../../../phase1/frontend

run app:
    python -m streamlit run app.py

    
Features:

| Function                | UI Element                                       |
| ----------------------- | ------------------------------------------------ |
| Send JSON from frontend | Text editor + send button                        |
| Upload CSV file         | Drag-and-drop CSV uploader                       |
| Run inference           | Button → displays class result, table, and graph |
| Export results          | Download CSV button                              |
| Brand Identity          | Title, tagline, modern UI layout                 |
