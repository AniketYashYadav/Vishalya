import 'package:flutter/material.dart';
import '../lib/api_service.dart';
import '../lib/patient_model.dart';

void main() => runApp(const VishalyaTestApp());

class VishalyaTestApp extends StatelessWidget {
  const VishalyaTestApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text("Vishalya API Test")),
        body: Center(
          child: ElevatedButton(
            onPressed: () async {
              // Creating a Dummy High-Risk Patient
              final dummyPatient = PatientModel(
                patientId: "P-9999",
                villagePin: "201310",
                timestamp: DateTime.now().toIso8601String(),
                symptoms: {
                  "fever": 1,
                  "cough": 1,
                  "shortness_of_breath": 1,
                  // Baaki sab apne aap 0 le lega due to model logic
                },
              );

              // Calling Ashish's API
              final result = await ApiService().predictRisk(dummyPatient);
              
              if (result != null) {
                print("✅ ML Prediction: ${result['status']}");
              } else {
                print("⚠️ API Hit Failed!");
              }
            },
            child: const Text("Test ML Pipeline Hit"),
          ),
        ),
      ),
    );
  }
}