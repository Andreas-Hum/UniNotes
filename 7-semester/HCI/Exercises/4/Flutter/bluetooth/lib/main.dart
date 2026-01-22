import 'dart:async';
import 'package:flutter/material.dart';
import 'package:bluetooth_low_energy/bluetooth_low_energy.dart';
import 'package:permission_handler/permission_handler.dart';

void main() {
  runApp(const MaterialApp(
    debugShowCheckedModeBanner: false,
    home: EmojiBluetoothWatchApp(),
  ));
}

class EmojiBluetoothWatchApp extends StatefulWidget {
  const EmojiBluetoothWatchApp({super.key});

  @override
  State<EmojiBluetoothWatchApp> createState() => _EmojiBluetoothWatchAppState();
}

class _EmojiBluetoothWatchAppState extends State<EmojiBluetoothWatchApp> {
  // --- BLUETOOTH LOGIC ---
  final CentralManager _centralManager = CentralManager();
  final PeripheralManager _peripheralManager = PeripheralManager();
  final TextEditingController _textController = TextEditingController();
  
  // Data Storage
  final List<String> _emojiFeed = [];
  final Map<String, String> _lastMessageFromPeer = {};
  
  StreamSubscription? _discoverySubscription;
  bool _isAdvertising = false;

  @override
  void initState() {
    super.initState();
    _initWatchBluetooth();
  }

  Future<void> _initWatchBluetooth() async {
    // 1. Request all permissions upfront
    await [
      Permission.bluetooth,
      Permission.bluetoothScan,
      Permission.bluetoothAdvertise,
      Permission.bluetoothConnect,
      Permission.location,
    ].request();

    // 2. Authorize managers [cite: 17, 26]
    await _centralManager.authorize();
    await _peripheralManager.authorize();

    // 3. Start scanning logic
    _startScanning();
  }

  void _startScanning() async {
    _discoverySubscription = _centralManager.discovered.listen((eventArgs) {
      final advertisement = eventArgs.advertisement;
      final String? name = advertisement.name;

      // Filter for "sHCI:" prefix [cite: 12]
      if (name != null && name.startsWith("sHCI:")) {
        _handleNewDiscovery(eventArgs.peripheral.uuid.toString(), name);
      }
    });

    await _centralManager.startDiscovery(); // [cite: 44]
  }

  void _handleNewDiscovery(String uuid, String rawName) {
    // Strip prefix
    String message = rawName.substring(5);

    // Deduplication: Only update if the message has changed for this specific user [cite: 6]
    if (_lastMessageFromPeer[uuid] != message) {
      setState(() {
        _lastMessageFromPeer[uuid] = message;
        // Add to top of list [cite: 5]
        _emojiFeed.insert(0, message);
      });
    }
  }

  Future<void> _broadcastEmoji() async {
    String emoji = _textController.text.trim();
    if (emoji.isEmpty) return;

    // Create payload "sHCI:😎"
    String broadcastName = "sHCI:$emoji";

    // Stop old ad before starting new one [cite: 20]
    if (_isAdvertising) {
      await _peripheralManager.stopAdvertising();
    }

    final advertisement = Advertisement(name: broadcastName);
    await _peripheralManager.startAdvertising(advertisement);

    setState(() {
      _isAdvertising = true;
      _emojiFeed.insert(0, "Me: $emoji");
      _textController.clear();
    });
  }

  @override
  void dispose() {
    _centralManager.stopDiscovery();
    _peripheralManager.stopAdvertising();
    _discoverySubscription?.cancel();
    _textController.dispose();
    super.dispose();
  }

  // --- WATCH UI ---
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Black background is standard for Wear OS to save battery
      backgroundColor: Colors.black,
      
      // Center and Padding are critical for round screens
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14.0, vertical: 18.0),
          child: Column(
            children: [
              // Tiny Header
              const Text(
                "sHCI Broadcast",
                style: TextStyle(color: Colors.blueGrey, fontSize: 10),
              ),
              
              const Divider(color: Colors.white24),

              // The List
              Expanded(
                child: _emojiFeed.isEmpty
                    ? const Center(
                        child: Text(
                          "Scanning...",
                          style: TextStyle(color: Colors.grey, fontSize: 12),
                        ),
                      )
                    : ListView.builder(
                        itemCount: _emojiFeed.length,
                        itemBuilder: (context, index) {
                          return Center(
                            child: Padding(
                              padding: const EdgeInsets.symmetric(vertical: 2.0),
                              child: Text(
                                _emojiFeed[index],
                                style: const TextStyle(
                                  fontSize: 24, 
                                  color: Colors.white
                                ),
                              ),
                            ),
                          );
                        },
                      ),
              ),

              const Divider(color: Colors.white24),

              // Input Field
              SizedBox(
                height: 40,
                child: TextField(
                  controller: _textController,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white),
                  // 'send' action lets you broadcast from the keyboard
                  textInputAction: TextInputAction.send,
                  onSubmitted: (_) {
                     _broadcastEmoji();
                     // Unfocus to hide keyboard and see the list
                     FocusManager.instance.primaryFocus?.unfocus();
                  },
                  decoration: const InputDecoration(
                    hintText: "Emoji",
                    hintStyle: TextStyle(color: Colors.grey),
                    isDense: true,
                    border: InputBorder.none,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}