import { Text, StyleSheet, View, TouchableOpacity, ScrollView } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";

export default function Index() {
  const router = useRouter();

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.titleSection}>
          <Text style={styles.title}>Retirement Guidance</Text>
          <View style={styles.underline} />
        </View>

        {/* Description */}
        <Text style={styles.description}>
          Professional support to help you understand your retirement benefits, explore available resources, and make informed decisions for your future.
        </Text>

        {/* Button */}
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.push("/chat")}
          activeOpacity={0.8}
        >
          <Ionicons name="chatbubble-outline" size={20} color="#FFFFFF" style={styles.buttonIcon} />
          <Text style={styles.buttonText}>Begin Consultation</Text>
        </TouchableOpacity>

        {/* Features Section */}
        <View style={styles.featuresContainer}>
          <View style={styles.feature}>
            <Text style={styles.featureTitle}>Confidential Support</Text>
            <Text style={styles.featureDescription}>
              Your information and conversations remain private and secure
            </Text>
          </View>

          <View style={styles.feature}>
            <Text style={styles.featureTitle}>Expert Guidance</Text>
            <Text style={styles.featureDescription}>
              Access to comprehensive retirement benefit information
            </Text>
          </View>

          <View style={styles.feature}>
            <Text style={styles.featureTitle}>Local Resources</Text>
            <Text style={styles.featureDescription}>
              Connect with services and support in your community
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0a1929", // Dark blue background
  },
  content: {
    flex: 1,
    padding: 20,
    paddingTop: 60,
    alignItems: "center",
  },
  titleSection: {
    alignItems: "center",
    marginBottom: 30,
  },
  title: {
    fontSize: 42,
    fontWeight: "bold",
    color: "#FFFFFF",
    textAlign: "center",
    marginBottom: 8,
  },
  underline: {
    width: 120,
    height: 3,
    backgroundColor: "#d32f2f", // Red underline
    marginTop: 4,
  },
  description: {
    fontSize: 16,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 24,
    marginBottom: 40,
    paddingHorizontal: 20,
  },
  button: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#283593", // Dark blue button
    borderWidth: 2,
    borderColor: "#5c6bc0", // Light blue border
    borderRadius: 8,
    paddingVertical: 16,
    paddingHorizontal: 32,
    marginBottom: 60,
    minWidth: 200,
  },
  buttonIcon: {
    marginRight: 10,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "600",
  },
  featuresContainer: {
    width: "100%",
    flexDirection: "row",          // lay children out horizontally
    justifyContent: "space-between",
    paddingHorizontal: 10,
    marginTop: 40,
  },
  feature: {
    flex: 1,                       // each column gets equal width
    marginHorizontal: 8,
  },
  featureTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 8,
    textAlign: "left",             // align like the inspiration
  },
  featureDescription: {
    fontSize: 14,
    color: "#FFFFFF",
    textAlign: "left",             // align like the inspiration
    lineHeight: 20,
    opacity: 0.9,
  },
});