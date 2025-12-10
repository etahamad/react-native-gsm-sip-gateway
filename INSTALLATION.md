# Installation Guide

This guide will walk you through building and installing the Telon GSM-SIP Gateway app on your Android device.

## Prerequisites

- Android device running Android 8.0 (Oreo) or higher
- Root access (for Magisk module installation)
- GSM SIM card with active service
- Network connectivity for SIP registration

## Method 1: Using GitHub Actions (Recommended)

This is the easiest method as it doesn't require setting up a local development environment.

### Step 1: Trigger the Build

1. Go to your GitHub repository
2. Navigate to the **Actions** tab
3. Select the **Build Android App** workflow from the left sidebar
4. Click **Run workflow** button (top right)
5. Select the branch you want to build (usually `main` or `master`)
6. Click the green **Run workflow** button

Alternatively, the workflow will automatically run when you push changes to any branch.

### Step 2: Wait for Build to Complete

1. Click on the running workflow to see the build progress
2. Wait for all steps to complete (usually takes 5-15 minutes)
3. The workflow will show a green checkmark ✅ when successful

### Step 3: Download the APK

1. In the workflow run page, scroll down to the **Artifacts** section
2. You'll see `android-apk` artifact listed
3. Click on `android-apk` to download it (it downloads as a ZIP file)
4. Extract the ZIP file on your computer to get the `.apk` file

**Note**: The APK file will be named something like `app-release.apk` or `app-release-unsigned.apk`

### Step 4: Enable Installation from Unknown Sources

Before installing the APK, you need to allow your device to install apps from unknown sources:

#### For Android 8.0 and above:
1. Go to **Settings** > **Apps** (or **Application Manager**)
2. Tap the three-dot menu (⋮) or **Special access**
3. Select **Install unknown apps**
4. Choose your file manager or browser (e.g., **Files**, **Chrome**, **Downloads**)
5. Toggle **Allow from this source** to ON

#### For older Android versions:
1. Go to **Settings** > **Security**
2. Enable **Unknown sources** (toggle it ON)

### Step 5: Transfer APK to Your Phone

Choose one of these methods:

#### Method A: Email
1. Email the APK file to yourself
2. Open the email on your phone
3. Download the attachment

#### Method B: USB Cable
1. Connect your phone to your computer via USB
2. Enable **File Transfer** mode on your phone
3. Copy the APK file to your phone's Downloads folder
4. Disconnect the USB cable

#### Method C: Cloud Storage
1. Upload the APK to Google Drive, Dropbox, or similar service
2. Open the cloud storage app on your phone
3. Download the APK file

#### Method D: ADB (Advanced)
If you have ADB installed:
```bash
adb install path/to/app-release.apk
```

### Step 6: Install the APK

1. Open your file manager on your phone
2. Navigate to where you saved the APK (usually **Downloads** folder)
3. Tap on the APK file
4. Tap **Install** when prompted
5. Wait for installation to complete
6. Tap **Open** or **Done**

### Step 7: Install Magisk Module (Required)

The app requires system-level permissions provided by a Magisk module:

1. Copy `magisk/gateway.zip` to your phone
2. Open **Magisk Manager** app
3. Go to **Modules** tab
4. Tap **Install from storage**
5. Select `gateway.zip`
6. Reboot your device when prompted

## Method 2: Build Locally

If you prefer to build the app on your own machine:

### Prerequisites for Local Build

- Node.js 12.x
- Java JDK 8
- Android Studio with Android SDK
- Android NDK r17b

### Build Steps

1. **Install Dependencies**:
   ```bash
   cd telon-gateway-app
   npm install
   ```

2. **Build the APK**:
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

3. **Find the APK**:
   The APK will be located at:
   ```
   telon-gateway-app/android/app/build/outputs/apk/release/app-release.apk
   ```

4. **Install on Phone**:
   Follow steps 4-7 from Method 1 above.

## Troubleshooting

### APK Installation Fails

**Problem**: "App not installed" or "Installation blocked"

**Solutions**:
- Make sure "Unknown sources" is enabled for your file manager
- Check if you have enough storage space
- Try uninstalling any previous version of the app first
- Ensure the APK file wasn't corrupted during download (re-download if needed)

### Build Fails in GitHub Actions

**Problem**: Workflow fails with errors

**Solutions**:
- Check the workflow logs for specific error messages
- Ensure all required secrets are set (if using release keystore)
- Verify that the repository structure is correct
- Check if Node.js version compatibility issues exist

### App Crashes After Installation

**Problem**: App crashes immediately after opening

**Solutions**:
- Ensure Magisk module is installed and device is rooted
- Check that all required permissions are granted
- Verify device compatibility (Android 8.0+)
- Check device logs: `adb logcat | grep -i gateway`

### SIP Registration Fails

**Problem**: App installs but can't connect to SIP server

**Solutions**:
- Verify network connectivity (WiFi or mobile data)
- Check SIP server address (default: 192.168.88.254)
- Ensure firewall isn't blocking SIP traffic
- Verify device ID is recognized (check app logs)

## Security Notes

⚠️ **Important Security Considerations**:

1. **Unknown Sources**: Remember to disable "Unknown sources" after installation for security
2. **APK Source**: Only install APKs from trusted sources (your own builds or official releases)
3. **Root Access**: Rooting your device and installing Magisk modules can void warranty and pose security risks
4. **Permissions**: This app requires extensive permissions - review them carefully before installation

## Verifying Installation

After installation, verify the app is working:

1. Open the **Telon GSM-SIP Gateway** app
2. Check the logs in the app - you should see SIP registration status
3. Verify device ID is detected correctly
4. Test with a SIP call to verify gateway functionality

## Updating the App

To update to a newer version:

1. Build a new APK using GitHub Actions or locally
2. Download the new APK
3. Install it over the existing app (no need to uninstall)
4. The app will be updated automatically

## Support

If you encounter issues not covered in this guide:

- Check the main [README.md](README.md) for troubleshooting tips
- Review the app logs for error messages
- Visit [telon.org](https://telon.org) for additional support
- Contact support at [support@telon.org](mailto:support@telon.org)

