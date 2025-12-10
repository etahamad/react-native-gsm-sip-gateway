module.exports = {
  presets: [
    [
      'module:metro-react-native-babel-preset',
      {
        unstable_transformProfile: 'hermes-stable',
      },
    ],
    [
      '@babel/preset-typescript',
      {
        allowNamespaces: true,
        allowDeclareFields: true,
        isTSX: false,
        onlyRemoveTypeImports: true,
      },
    ],
  ],
};
