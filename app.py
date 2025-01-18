from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    output_image = remove(input_image)
    
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")