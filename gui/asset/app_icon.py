import os
import sys

app_icon_str = b'R0lGODlhZABkAIABAAAAAP///yH5BAEKAAEALAAAAABkAGQAAAL+jI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zgC+zzv9hsRgiIhEGjfJZnF5cUp/0Mr0CqhKsFjtg8v1NsBhcYJcNh/QaTO7LX531YH5+UrHL+xePsJfBWgguERIaGSo5zbVoxjnuAapJSc5SSlFN3jZlFm3qdTp+UkVOkoaKrqJ+ve5ykrpescW2whG63B4Kzuk2+vLktUSXMM4Uoli+0G28sbRjCyncWmiGlUtMmphir09YQqk/D0MIQ4iPo577nEO/qXewY6+F+8cL79bzmTvzl5fjM9pzLFjFATlSvQPg0GCqZzUwiSt0sGBDCMsTKgAIcReDBc3zsMYCaQViQw1BoxIL10/f/lUvtP3UmBMlC1ddoNX02a2dTl1TjN3c8vOI61GXuMGy1rSEksVPoO2jCUcIVNhilThkOnJX1y7ev0KNqzYsWTLmj2LNq3atR0KAAA7'

__asset_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
app_icon_ico = os.path.join(__asset_dir, 'icon.ico')
