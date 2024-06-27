// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use chrono;
use std::fs::OpenOptions;
use std::io::Write;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![write_log])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command(rename_all = "snake_case")]
fn write_log(log_message: String) {
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open("logs.txt")
        .expect("Unable to access logs.txt file");
    let log_with_timestamp = format!(
        "[{}] {}\n",
        chrono::Local::now().format("%Y-%m-%d %H:%M:%S"),
        log_message
    );
    if let Err(e) = file.write_all(log_with_timestamp.as_bytes()) {
        eprintln!("Couldn't write to file: {}", e);
    }
}