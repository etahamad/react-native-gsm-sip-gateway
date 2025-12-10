
import React, { Component } from 'react';
import {NativeModules} from 'react-native';

import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
} from 'react-native';

// Colors definition (replacing deprecated NewAppScreen import)
const Colors = {
  lighter: '#F3F3F3',
  light: '#DAE1E7',
  dark: '#444444',
  black: '#000000',
  white: '#FFFFFF',
};

//import {ReplaceDialer} from 'react-native-replace-dialer';

export default class App extends Component {
  constructor() {
    super();
    var ConsolePanel = require('react-native-console-panel').displayWhenDev();
  }
  
  

  async componentDidMount() {
    //
    //await this.tGateway.onMount();
    /*
      let tReplaceDialer = new ReplaceDialer();
  
                tReplaceDialer.isDefaultDialer((data) => {
                    if (data)
                      console.log('Is ALREADY default dialer.');
                    else {
                      console.log('Is NOT default dialer, try to set.');
                      tReplaceDialer.setDefaultDialer((data) => {
                        if (data) {
                          console.log('Default dialer sucessfully set.');
                        } else {
                          console.log('Default dialer NOT set');
                        }
                      });
                    }
                  });
                  */
            
        console.log(this.tGateway);
        //console.log(this.tGateway.txtLog);
      
  }


  render() {



    return (
      <>
        <StatusBar barStyle="dark-content" />
        <SafeAreaView>
          <ScrollView
            contentInsetAdjustmentBehavior="automatic"
            style={styles.scrollView}>
            

            <View style={styles.body}>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Gateway log</Text>
                {ConsolePanel}
              </View>
            </View>
          </ScrollView>
        </SafeAreaView>
      </>
    );
  };
}

/*
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>See Your Changes</Text>
                <Text style={styles.sectionDescription}>
                  <ReloadInstructions />
                </Text>
              </View>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Debug</Text>
                <Text style={styles.sectionDescription}>
                  <DebugInstructions />
                </Text>
              </View>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Learn More</Text>
                <Text style={styles.sectionDescription}>
                  Read the docs to discover what to do next:
              </Text>
              </View>
              <LearnMoreLinks />

*/
const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: Colors.lighter,
  },
  engine: {
    position: 'absolute',
    right: 0,
  },
  body: {
    backgroundColor: Colors.white,
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: Colors.black,
  },
  sectionDescription: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: '400',
    color: Colors.dark,
  },
  highlight: {
    fontWeight: '700',
  },
  footer: {
    color: Colors.dark,
    fontSize: 12,
    fontWeight: '600',
    padding: 4,
    paddingRight: 12,
    textAlign: 'right',
  },
});


