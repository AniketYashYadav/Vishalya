import 'dart:convert';
import 'package:http/http.dart' as http;
import 'patient_model.dart';

class ApiService {
  // REPLACE this with Ashish's local IP or Ngrok URL during testing
  static const String baseUrl = 'http://192.168.1.xxx:8000'; 

  Future<Map<String, dynamic>?> predictRisk(PatientModel patient) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/predict_risk'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(patient.toJson()),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body); // Success Response
      } else {
        print("❌ Server Error: ${response.statusCode}");
        return null;
      }
    } catch (e) {
      print("❌ Connection Failed: $e");
      // Yahan hum local SQLite mein save karne ka logic call karenge
      return null; 
    }
  }
}