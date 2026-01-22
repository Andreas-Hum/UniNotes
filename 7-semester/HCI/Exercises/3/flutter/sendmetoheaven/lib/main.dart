import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart'; // For locking orientation
import 'package:sensors_plus/sensors_plus.dart';

void main() {
  runApp(const SimpleThrowApp());
}

class SimpleThrowApp extends StatelessWidget {
  const SimpleThrowApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const ThrowPage(),
      theme: ThemeData.dark(), // Dark mode looks better
    );
  }
}

class ThrowPage extends StatefulWidget {
  const ThrowPage({super.key});

  @override
  State<ThrowPage> createState() => _ThrowPageState();
}

class _ThrowPageState extends State<ThrowPage> {
  // Sensors
  StreamSubscription<AccelerometerEvent>? _subscription;
  
  // Data
  String _status = "READY"; // READY, IN AIR, CAUGHT
  Color _bgColor = Colors.black;
  double _resultHeight = 0.0;
  
  // Logic
  DateTime? _airTimeStart;
  bool _inFreeFall = false;

  @override
  void initState() {
    super.initState();
    // Lock screen so it doesn't rotate while throwing
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
    _startListening();
  }

  void _startListening() {
    // We check the sensor very fast (every 20ms is default)
    _subscription = accelerometerEventStream().listen((event) {
      
      // Calculate Total G-Force
      // x, y, z are the forces on the phone axes
      double gForce = sqrt(event.x * event.x + event.y * event.y + event.z * event.z);

      // LOGIC:
      // 1. Earth gravity is roughly 9.8. 
      // 2. If you drop/throw the phone, gForce goes close to 0.
      
      if (gForce < 2.0) { 
        // We are in the air (Free Fall)
        if (!_inFreeFall) {
          _startFreeFall();
        }
      } else {
        // We are holding it, or we just caught it
        if (_inFreeFall) {
          _endFreeFall();
        }
      }
    });
  }

  void _startFreeFall() {
    setState(() {
      _inFreeFall = true;
      _status = "IN AIR!";
      _bgColor = Colors.blueAccent;
      _airTimeStart = DateTime.now(); // Start the stopwatch
    });
  }

  void _endFreeFall() {
    if (_airTimeStart == null) return;

    DateTime now = DateTime.now();
    // How many milliseconds was it flying?
    int flightTimeMs = now.difference(_airTimeStart!).inMilliseconds;
    
    // Ignore small jitters (must be in air for at least 0.2 seconds)
    if (flightTimeMs > 200) {
      _calculateHeight(flightTimeMs);
    } else {
      // Reset if it was just noise
      setState(() {
        _status = "READY";
        _bgColor = Colors.black;
      });
    }

    _inFreeFall = false;
    _airTimeStart = null;
  }

  void _calculateHeight(int flightTimeMs) {
    // PHYSICS FORMULA:
    // We assume time up = time down. So we divide total time by 2.
    double timeSeconds = flightTimeMs / 1000.0;
    double timeUp = timeSeconds / 2.0;
    
    // Height = 1/2 * g * t^2
    double gravity = 9.81;
    double height = 0.5 * gravity * (timeUp * timeUp);

    setState(() {
      _resultHeight = height;
      _status = "CAUGHT!";
      _bgColor = Colors.green[800]!;
    });

    // Reset back to Ready after 3 seconds
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) {
        setState(() {
          _status = "READY";
          _bgColor = Colors.black;
        });
      }
    });
  }

  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _bgColor,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              _status,
              style: const TextStyle(
                fontSize: 40, 
                fontWeight: FontWeight.bold, 
                color: Colors.white
              ),
            ),
            const SizedBox(height: 50),
            if (_resultHeight > 0)
              Column(
                children: [
                  Text(
                    _resultHeight.toStringAsFixed(2),
                    style: const TextStyle(
                      fontSize: 100, 
                      fontWeight: FontWeight.bold, 
                      color: Colors.white
                    ),
                  ),
                  const Text(
                    "METERS",
                    style: TextStyle(fontSize: 20, color: Colors.white70),
                  ),
                ],
              ),
            if (_resultHeight == 0)
               const Text(
                "Throw straight up\nand catch it!",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white54, fontSize: 18),
              ),
          ],
        ),
      ),
    );
  }
}