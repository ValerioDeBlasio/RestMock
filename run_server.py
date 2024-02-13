# ------- #
# Created by: valeriodeblasio with ❤️
# Date: Tue 13/02/2024
# Time: 10:41
# ------- #
import uvicorn

from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5023)
