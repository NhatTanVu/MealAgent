import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { usePlanWizard } from "@/context/planWizard";
import { api } from "@/services/api";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet } from "react-native";

export default function PlanStep2() {
    const { inputs, candidates, setCandidates, setResult } = usePlanWizard();
    const [loading, setLoading] = useState(true);
    const router = useRouter();
    const choose = (id: number, title: string) => {
        setLoading(true);
        try {
            // ✅ Replace with real backend compute later:
            // POST /agent/run -> returns grocery + steps
            // For now, create a demo result:
            setResult({
                recipeId: id,
                title,
                ingredientsHave: inputs.ingredients,
                ingredientsMissing: ["salt", "garlic"],
                steps: ["Prep ingredients", "Cook main protein", "Add veggies", "Serve"]
            });
            router.push("/plan/step3");
        }
        finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const loadCandidates = async () => {
            setLoading(true);
            const res = await api.post("/agent/plan", inputs);
            const data = await res.data["candidates"] as [];

            try {
                console.log(data);
                setCandidates(data.map((d) => ({
                    "id": d["id"],
                    "title": d["title"],
                    "scoreReason": d["score_reason"]
                })));
            } finally {
                setLoading(false);
            }
        };
        loadCandidates();
    }, []);

    if (loading) {
        return (
            <ThemedView style={styles.center}>
                <ActivityIndicator size="large" />
                <ThemedText>Finding best recipes...</ThemedText>
            </ThemedView>
        );
    }

    return (
        <ThemedView style={styles.container}>
            <ThemedText style={styles.h1}>Pick a recipe</ThemedText>
            {
                candidates.map((c) => (
                    <Pressable key={c.id} style={styles.card} onPress={() => choose(c.id, c.title)}>
                        <ThemedText style={styles.title}>{c.title}</ThemedText>
                        <ThemedText style={styles.reason}>{c.scoreReason}</ThemedText>
                    </Pressable>
                ))
            }
            <Pressable onPress={() => router.push("/plan/step1")} style={styles.secondaryBtn}>
                <ThemedText style={styles.secondaryBtnText}>Back</ThemedText>
            </Pressable>
        </ThemedView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1, padding: 20, gap: 12
    },
    h1: {
        fontSize: 22, fontWeight: "700"
    },
    card: {
        backgroundColor: "#f5f5f5", padding: 16, borderRadius: 10, gap: 6
    },
    title: {
        fontSize: 16, fontWeight: "700"
    },
    reason: {
        color: "#555"
    },
    secondaryBtn: {
        marginTop: 10, padding: 14, borderRadius: 10, alignItems: "center", borderWidth: 1, borderColor: "#ccc"
    },
    secondaryBtnText: {
        fontWeight: "700"
    },
    center: {
        flex: 1, alignItems: "center", justifyContent: "center", gap: 10
    }
});