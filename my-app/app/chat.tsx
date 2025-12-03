import React, { useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";

type Message = {
  id: string;
  from: "user" | "assistant";
  text: string;
};

const QUICK_QUESTIONS = [
  "What is Medicare Part A?",
  "When should I enroll in Medicare?",
  "What's the difference between Medicare and Medicaid?",
  "Find local senior resources",
];

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      from: "assistant",
      text: "Hi! I'm here to help you understand your Medicare and retirement options. What questions do you have today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleSend = async (text?: string) => {
    const content = (text ?? input).trim();
    if (!content || isSending) return;

    setIsSending(true);
    setInput("");

    // Add user message immediately
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      from: "user",
      text: content,
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: content }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data: { reply?: string } = await response.json();
      const replyText =
        data.reply ??
        "I had trouble reading the response from the retirement assistant. Please try asking your question again in a moment.";

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        from: "assistant",
        text: replyText,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error", error);
      const errorMessage: Message = {
        id: `assistant-error-${Date.now()}`,
        from: "assistant",
        text:
          "I’m sorry — I couldn’t reach the retirement resources assistant service. Please check that the backend server is running and try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        {/* Sidebar */}
        <View style={styles.sidebar}>
          <View style={styles.sidebarHeader}>
            <View style={styles.avatar}>
              <Ionicons name="home" size={22} color="#FFFFFF" />
            </View>
            <View>
              <Text style={styles.sidebarTitle}>Retirement Assistant</Text>
              <Text style={styles.sidebarSubtitle}>Medicare & Resources</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.profileButton} activeOpacity={0.9}>
            <View style={styles.profileIconCircle}>
              <Ionicons name="person-outline" size={18} color="#FFFFFF" />
            </View>
            <Text style={styles.profileText}>Your Profile</Text>
            <Ionicons name="information-circle-outline" size={16} color="#A0AEC0" />
          </TouchableOpacity>

          <Text style={styles.quickQuestionsTitle}>Quick Questions</Text>

          <View style={styles.quickQuestionsList}>
            {QUICK_QUESTIONS.map((q) => (
              <TouchableOpacity
                key={q}
                style={styles.quickQuestionButton}
                activeOpacity={0.9}
                onPress={() => handleSend(q)}
              >
                <Text style={styles.quickQuestionText}>{q}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <View style={styles.noteBox}>
            <Text style={styles.noteLabel}>Note:</Text>
            <Text style={styles.noteText}>
              This tool provides general guidance only. Always verify with official
              sources and consult professionals for your specific situation.
            </Text>
          </View>
        </View>

        {/* Chat area */}
        <View style={styles.chatArea}>
          <ScrollView
            style={styles.messagesContainer}
            contentContainerStyle={styles.messagesContent}
          >
            {messages.map((m) => (
              <View
                key={m.id}
                style={[
                  styles.messageBubble,
                  m.from === "assistant"
                    ? styles.assistantBubble
                    : styles.userBubble,
                ]}
              >
                <Text style={styles.messageText}>{m.text}</Text>
              </View>
            ))}
          </ScrollView>

          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Ask about Medicare, retirement benefits, or local resources..."
              placeholderTextColor="#A0AEC0"
              value={input}
              onChangeText={setInput}
              multiline
            />
            <TouchableOpacity
              style={styles.sendButton}
              onPress={() => handleSend()}
              activeOpacity={0.9}
            >
              <Ionicons name="send" size={20} color="#FFFFFF" />
            </TouchableOpacity>
          </View>

          <Text style={styles.footerText}>
            Preliminary guidance only. Always verify with official sources and
            consult professionals for financial decisions.
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#0a1929",
  },
  container: {
    flex: 1,
    flexDirection: "row",
    backgroundColor: "#0a1929",
  },
  sidebar: {
    width: 320,
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: 16,
    backgroundColor: "#0b1f33",
    borderRightWidth: StyleSheet.hairlineWidth,
    borderRightColor: "#1E293B",
  },
  sidebarHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 24,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#00ACC1",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
  },
  sidebarTitle: {
    fontSize: 18,
    fontWeight: "700",
    color: "#FFFFFF",
  },
  sidebarSubtitle: {
    fontSize: 13,
    color: "#A0AEC0",
    marginTop: 2,
  },
  profileButton: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#111827",
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderRadius: 12,
    marginBottom: 24,
  },
  profileIconCircle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: "#00ACC1",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 10,
  },
  profileText: {
    flex: 1,
    fontSize: 14,
    fontWeight: "600",
    color: "#FFFFFF",
  },
  quickQuestionsTitle: {
    fontSize: 14,
    fontWeight: "600",
    color: "#E5E7EB",
    marginBottom: 12,
  },
  quickQuestionsList: {
    marginBottom: 24,
  },
  quickQuestionButton: {
    backgroundColor: "#111827",
    borderRadius: 10,
    paddingVertical: 10,
    paddingHorizontal: 12,
    marginBottom: 8,
  },
  quickQuestionText: {
    fontSize: 14,
    color: "#E5E7EB",
  },
  noteBox: {
    marginTop: "auto",
    padding: 12,
    borderRadius: 12,
    backgroundColor: "#FFFBEB",
  },
  noteLabel: {
    fontSize: 13,
    fontWeight: "700",
    color: "#92400E",
    marginBottom: 4,
  },
  noteText: {
    fontSize: 12,
    color: "#78350F",
  },
  chatArea: {
    flex: 1,
    paddingHorizontal: 32,
    paddingTop: 24,
    paddingBottom: 16,
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    paddingBottom: 16,
  },
  messageBubble: {
    maxWidth: "80%",
    padding: 14,
    borderRadius: 16,
    marginBottom: 10,
  },
  assistantBubble: {
    alignSelf: "flex-start",
    backgroundColor: "#111827",
  },
  userBubble: {
    alignSelf: "flex-end",
    backgroundColor: "#00ACC1",
  },
  messageText: {
    fontSize: 14,
    color: "#F9FAFB",
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#111827",
    borderRadius: 999,
    paddingHorizontal: 18,
    paddingVertical: 8,
    marginTop: 8,
  },
  input: {
    flex: 1,
    color: "#F9FAFB",
    fontSize: 14,
    paddingVertical: 6,
    marginRight: 10,
  },
  sendButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#00ACC1",
    alignItems: "center",
    justifyContent: "center",
  },
  footerText: {
    marginTop: 8,
    fontSize: 11,
    color: "#9CA3AF",
    textAlign: "center",
  },
});


