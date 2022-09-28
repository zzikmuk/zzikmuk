import React, { useEffect } from "react";
import { StyleSheet, Text, View } from "react-native";
import CarouselOrganism from "../organism/CarouselOrganism";
import { fetchRecipes } from "../../apis/recipes";
import axios from "axios";

export default function MainPage({ navigation }) {
  ///// test api /////
  function requestTestSuccess(response) {
    console.log(response.data);
  }

  function requestTestFail(error) {
    console.log(error.response);
  }

  useEffect(() => {
    fetchRecipes(requestTestSuccess, requestTestFail);
  }, []);
  ///// test api /////

  return (
    <View style={styles.container}>
      <View style={styles.logoBoxText}>
        <Text style={styles.logoText} onPress={() => navigation.navigate("Main")}>
          ZZIKMUK
        </Text>
      </View>
      <Text style={styles.popularText}>
        🔥 오늘 인기 있는 <Text style={styles.RecipeText}>레시피</Text> 🔥
      </Text>
      <View style={styles.carousel}>
        <CarouselOrganism />
      </View>
      <Text style={styles.tipText}>🍯 요리 꿀팁 🍯</Text>
      <View style={styles.tipRandom}>
        <Text style={styles.tipContent}>
          계란을 삶을 때 소금과 식초를 넣어주면 계란이 깨지지 않고 껍질을 쉽게 분리하게 해줍니다.
        </Text>
      </View>
      <View style={styles.empty}></View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  logoBoxText: {
    backgroundColor: "#FFFFFF",
    alignSelf: "stretch",
    height: 60,
    justifyContent: "center",
    elevation: 5,
  },
  logoText: {
    fontSize: 26,
    fontWeight: "bold",
    color: "#FDB954",
    textAlign: "center",
  },
  popularText: {
    marginTop: 30,
    flex: 1,
    fontSize: 22,
    fontWeight: "bold",
  },
  carousel: {
    flex: 10,
  },

  RecipeText: {
    color: "#FF8B34",
  },
  tipText: {
    flex: 1,
    marginTop: 30,
    fontSize: 22,
    fontWeight: "bold",
  },
  tipRandom: {
    flex: 2,
    marginTop: 10,
    width: 330,
    height: 80,
  },
  tipContent: {
    fontSize: 16,
    backgroundColor: "#FFE48E",
    borderRadius: 10,
    elevation: 2,
  },
  empty: {
    flex: 1,
  },
});
