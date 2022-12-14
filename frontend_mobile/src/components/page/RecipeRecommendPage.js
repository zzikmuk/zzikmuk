import React, { useEffect, useState, useRef } from "react";
import { StyleSheet, View, Pressable, ScrollView } from "react-native";
import { AntDesign } from "@expo/vector-icons";
import Card from "../organism/Card";
import TopNav from "../organism/TopNav";
import { fetchRecommendRecipeList } from "../../apis/recipes";
import Loading from "../atom/Loading";

export default function RecipeRecommendPage({ route, navigation }) {
  const [recommendList, setRecommendList] = useState([]);
  const scrollView = useRef();

  function requestRecommendRecipeListSuccess(res) {
    setRecommendList(res.data);
  }

  function requestRecommendRecipeListFail(err) {
    setRecommendList([]);
  }

  useEffect(() => {
    fetchRecommendRecipeList(
      route.params.newIngredient,
      requestRecommendRecipeListSuccess,
      requestRecommendRecipeListFail,
    );
  }, []);

  function goToRecipe(id) {
    navigation.push("Recipe", { id });
  }

  return recommendList.length === 0 ? (
    <Loading />
  ) : (
    <View style={styles.container}>
      <TopNav title="추천 레시피" />
      <View style={styles.content}>
        <ScrollView ref={scrollView} showsVerticalScrollIndicator={false}>
          {recommendList.map((recipe, index) => (
            <Pressable onPress={() => goToRecipe(recipe[0])} key={index}>
              <Card name={recipe[1]} thumbnail={recipe[2]} difficulty={recipe[3]} amount={recipe[4]} time={recipe[5]} />
            </Pressable>
          ))}
        </ScrollView>
      </View>
      <Pressable onPress={() => scrollView.current.scrollTo({ y: 0 })}>
        <View style={styles.topBtn}>
          <AntDesign name="caretup" size={18} color="white" />
        </View>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff9f9",
  },
  content: {
    flex: 24,
    alignItems: "center",
  },
  topBtn: {
    position: "absolute",
    width: 45,
    height: 45,
    backgroundColor: "#FFE48E",
    bottom: 20,
    right: 20,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 40,
    opacity: 0.8,
  },
});
