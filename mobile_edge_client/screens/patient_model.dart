class PatientModel {
  final String patientId;
  final String villagePin;
  final String timestamp;
  final int medicineAvailable; // Feature 2: Medicine Check (1 = Yes, 0 = No)
  final double latitude;       // Feature 4: Geo-Tagging
  final double longitude;      // Feature 4: Geo-Tagging
  final Map<String, int> symptoms;

  PatientModel({
    required this.patientId,
    required this.villagePin,
    required this.timestamp,
    required this.medicineAvailable,
    required this.latitude,
    required this.longitude,
    required this.symptoms,
  });

  Map<String, dynamic> toJson() {
    return {
      "patient_id": patientId,
      "village_pin": villagePin,
      "timestamp": timestamp,
      "medicine_available": medicineAvailable,
      "latitude": latitude,
      "longitude": longitude,
      "symptoms": symptoms,
    };
  }
}