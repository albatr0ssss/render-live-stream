#!/bin/bash
mkdir -p /app/live_stream
# ব্যাকগ্রাউন্ডে অটো রেন্ডার চালু
python /app/auto_render.py &
# ফোল্ডারে গিয়ে Render-এর পোর্টে সার্ভার চালু
cd /app/live_stream
sleep 3
python -m http.server $PORT
