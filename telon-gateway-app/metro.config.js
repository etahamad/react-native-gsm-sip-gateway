/**
 * Metro configuration for React Native
 * https://github.com/facebook/react-native
 *
 * @format
 */

const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 *
 * @type {import('metro-config').MetroConfig}
 */
const config = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },
  resolver: {
    sourceExts: ['js', 'jsx', 'ts', 'tsx', 'json'],
    unstable_enablePackageExports: true,
  },
  serializer: {
    getModulesRunBeforeMainModule: () => [],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
