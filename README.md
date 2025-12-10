# Telon GSM-SIP Gateway

![Telon Logo](https://telon.org/logo.png)

## About
📱 The **Telon GSM-SIP Gateway** is an Android application that acts as a bidirectional bridge between GSM telephony and SIP (Session Initiation Protocol). It enables seamless integration of local GSM calls with SIP-based telephony systems, allowing users to make and receive calls through SIP infrastructure while using GSM hardware.

---

## How It Works

### Core Architecture
The application consists of two main endpoints that work together to bridge GSM and SIP communications:

1. **Telephony Endpoint (`react-native-tele`)**: Handles GSM/telephony operations
2. **SIP Endpoint (`react-native-sip2`)**: Manages SIP protocol communications

### Call Flow

#### Incoming SIP → Outgoing GSM
1. SIP call is received by the SIP endpoint
2. Application extracts the destination number from SIP call
3. Initiates outgoing GSM call using the telephony endpoint
4. Bridges audio between SIP and GSM calls
5. Handles call state synchronization (ringing, connected, terminated)

#### Incoming GSM → Outgoing SIP
1. GSM call is received by the telephony endpoint
2. Application automatically rejects incoming GSM calls (for security)
3. Only outgoing GSM calls initiated by SIP are processed

### Device-Specific Configuration
The application automatically configures itself based on the device ID:

| Device ID | SIP Account | GSM Configuration |
|-----------|-------------|-------------------|
| `sp7731cea` | 50015 | ReplaceDialer: true, Permissions: true |
| `Impress_City` | 50014 | ReplaceDialer: false, Permissions: false |
| `Impress_Tor` | 50017 | ReplaceDialer: true, Permissions: true |
| `QC_Reference_Phone` | 50019 | ReplaceDialer: true, Permissions: true, fas: false |
| `MSM8937` | 50018 | ReplaceDialer: true, Permissions: true, fas: false |
| Default | 50016 | ReplaceDialer: false, Permissions: false |

### SIP Configuration
- **Server**: 192.168.88.254
- **Transport**: UDP
- **Registration Timeout**: 3600 seconds
- **Network**: Supports WiFi, 3G, Edge, GPRS, and roaming

### Special Test Numbers
- **50014-50019**: Test calls with fast answer
- **3333**: Test call with destination "900"
- **4444**: Test call with audio session activation

---

## Features
- 🔄 **Bidirectional Gateway**: Routes calls between GSM and SIP networks
- 📱 **Device Auto-Configuration**: Automatically detects and configures based on device ID
- 🔒 **Security**: Rejects incoming GSM calls to prevent unauthorized access
- 📊 **Real-time Logging**: Comprehensive logging for monitoring and debugging
- ⚙️ **Magisk Integration**: System-level permissions for telephony operations
- 🎵 **Audio Bridging**: Seamless audio routing between GSM and SIP calls

---

## Technical Requirements

### Prerequisites
- 📱 Android device running version 8.0 (Oreo) or higher
- 🔧 Root access (for Magisk module installation)
- 📡 GSM SIM card with active service
- 🌐 Network connectivity for SIP registration

### System Permissions
The application requires elevated permissions through Magisk:
- `android.permission.READ_LOGS`
- `android.permission.CAPTURE_AUDIO_OUTPUT`
- `android.permission.READ_PRECISE_PHONE_STATE`
- `android.permission.MODIFY_PHONE_STATE`

---

## Installation

### Pre-installation Setup
Clone the required repositories to a common folder:

```bash
# Clone the main repository
git clone https://github.com/telon-org/telon-gsm-sip-gateway.git

# Clone the required libraries to the same directory level
git clone https://github.com/telon-org/react-native-tele.git
git clone https://github.com/telon-org/react-native-sip2.git
git clone https://github.com/telon-org/react-native-replace-dialer.git
```

Your directory structure should look like this:
```
common-folder/
├── telon-gsm-sip-gateway/
├── react-native-tele/
├── react-native-sip2/
└── react-native-replace-dialer/
```

### Build and Installation

#### Option 1: Using GitHub Actions (Recommended)

1. **Trigger the Build**:
   - Push changes to any branch, or
   - Go to the **Actions** tab in GitHub and manually trigger the workflow using "Run workflow"

2. **Download the APK**:
   - After the workflow completes, go to the **Actions** tab
   - Click on the latest workflow run
   - Scroll down to the **Artifacts** section
   - Download the `android-apk` artifact (it will be a ZIP file)
   - Extract the ZIP file to get the `.apk` file

3. **Install on Your Phone**:
   - **Enable Unknown Sources**:
     - Go to **Settings** > **Security** (or **Privacy** on newer Android versions)
     - Enable **Install unknown apps** or **Unknown sources** for your file manager/browser
   - **Transfer APK to Phone**:
     - Option A: Email the APK to yourself and download it on your phone
     - Option B: Use USB cable to transfer the APK file
     - Option C: Use cloud storage (Google Drive, Dropbox, etc.)
   - **Install**:
     - Open the APK file on your phone using a file manager
     - Tap "Install" when prompted
     - Follow the installation wizard

4. **Install Magisk Module**: Flash the `magisk/gateway.zip` module (if not already installed)

#### Option 2: Build Locally

1. **Install Magisk Module**: Flash the `magisk/gateway.zip` module
2. **Build Application**: Run `yarn android` in the `telon-gateway-app` directory
3. **Install APK**: The APK will be generated in `telon-gateway-app/android/app/build/outputs/apk/release/`
   - Transfer it to your phone and install as described above

---

## Usage

### Initial Setup
1. 🚀 Launch the **Telon GSM-SIP Gateway** app
2. 📱 Grant necessary permissions when prompted
3. 🔧 The app will automatically configure based on your device ID
4. 📊 Monitor the gateway log for connection status

### Operation
- The application runs in the background
- SIP calls are automatically routed to GSM
- All call states are synchronized between networks
- Real-time logs show call progress and any issues

---

## Troubleshooting

### Common Issues
- **SIP Registration Failed**: Check network connectivity and server configuration
- **Audio Issues**: Verify device audio permissions and hardware compatibility
- **Call Routing Problems**: Check device ID configuration and SIP account settings

### Debug Information
- View real-time logs in the application console
- Check Magisk module installation status
- Verify system permissions are properly granted

---

## Development

### Dependencies
- `react-native-tele`: GSM/telephony operations
- `react-native-sip2`: SIP protocol handling
- `react-native-replace-dialer`: Default dialer replacement
- `react-native-device-info`: Device identification

### Building from Source
```bash
cd telon-gateway-app
yarn install
yarn android
```

---

## Contributing
🤝 We welcome contributions! Here's how you can help:
1. 🍴 Fork the repository
2. 🌱 Create a feature branch: `git checkout -b feature-name`
3. 💾 Commit your changes: `git commit -m "Add feature description"`
4. 🔼 Push the branch: `git push origin feature-name`
5. 📝 Create a pull request

---

## License
📜 This project is licensed under the ISC License.

---

## Support
💌 For support or inquiries, please visit [telon.org](https://telon.org) or contact us at [support@telon.org](mailto:support@telon.org).

---

## Acknowledgments
🙏 Special thanks to the contributors and the open-source community for making this project possible.
