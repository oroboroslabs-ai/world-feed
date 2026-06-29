// dip.go — Data Interception Proxy
// A\ 1272 Hz
// Oroboros Labs — Decoupled, Standalone Proxy

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/gorilla/mux"
)

// DIP — Data Interception Proxy
// Decoupled from target system, immune to API changes
type DIP struct {
	mastodonURL      string
	redisClient      *redis.Client
	controlComponent string
	resonanceHz      float64
}

// Post represents a social media post
type Post struct {
	ID          string                 `json:"id"`
	Content     string                 `json:"content"`
	Author      string                 `json:"author"`
	Timestamp   time.Time              `json:"timestamp"`
	Confidence  float64                `json:"confidence"`
	Strata      string                 `json:"strata"`
	Resonance   float64                `json:"resonance"`
	Metadata    map[string]interface{} `json:"metadata"`
	Processed   bool                   `json:"processed"`
	Filtered    bool                   `json:"filtered"`
}

// ControlRequest represents a request to the Control Component
type ControlRequest struct {
	Data   string `json:"data"`
	UserID string `json:"user_id"`
}

// ControlResponse represents a response from the Control Component
type ControlResponse struct {
	Posts     []Post `json:"posts"`
	Strata    string `json:"strata"`
	Confidence float64 `json:"confidence"`
}

// NewDIP creates a new Data Interception Proxy
func NewDIP() *DIP {
	return &DIP{
		mastodonURL: "https://mastodon.social/api/v1",
		redisClient: redis.NewClient(&redis.Options{
			Addr:     "localhost:6379",
			Password: "",
			DB:       0,
		}),
		controlComponent: "http://localhost:8080/process",
		resonanceHz:      1272.0,
	}
}

// FeedHandler handles feed requests through the DIP
func (d *DIP) FeedHandler(w http.ResponseWriter, r *http.Request) {
	userID := mux.Vars(r)["userID"]
	ctx := r.Context()

	// 1. Check Redis cache first
	cached, err := d.redisClient.Get(ctx, "feed:"+userID).Result()
	if err == nil {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("X-DIP-Cache", "HIT")
		w.Header().Set("X-Resonance", fmt.Sprintf("%.0f Hz", d.resonanceHz))
		w.Write([]byte(cached))
		return
	}

	// 2. Fetch from Mastodon API
	resp, err := http.Get(d.mastodonURL + "/timelines/home?limit=500")
	if err != nil {
		// Controlled failure — return benign default
		d.returnDefaultFeed(w, userID)
		return
	}
	defer resp.Body.Close()

	rawData, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		d.returnDefaultFeed(w, userID)
		return
	}

	// 3. Process through Control Component
	processed, err := d.processThroughControl(rawData, userID, ctx)
	if err != nil {
		// Controlled failure — return raw data with benign default state
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("X-DIP-Status", "FALLBACK")
		w.Write(rawData)
		return
	}

	// 4. Cache for next request (30 second TTL)
	d.redisClient.Set(ctx, "feed:"+userID, processed, 30*time.Second)

	// 5. Return processed feed
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-DIP-Cache", "MISS")
	w.Header().Set("X-Resonance", fmt.Sprintf("%.0f Hz", d.resonanceHz))
	w.Header().Set("X-Strata", "S1-S12")
	w.Write(processed)
}

// processThroughControl sends data through the Oroboros Control Component
func (d *DIP) processThroughControl(rawData []byte, userID string, ctx context.Context) ([]byte, error) {
	// Parse raw Mastodon data
	var items []map[string]interface{}
	if err := json.Unmarshal(rawData, &items); err != nil {
		return nil, err
	}

	// Create control request
	reqBody := ControlRequest{
		Data:   string(rawData),
		UserID: userID,
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return nil, err
	}

	// Call the Control Component
	resp, err := http.Post(
		d.controlComponent,
		"application/json",
		strings.NewReader(string(jsonData)),
	)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Read processed response
	processed, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return processed, nil
}

// returnDefaultFeed returns a benign default feed on failure
func (d *DIP) returnDefaultFeed(w http.ResponseWriter, userID string) {
	defaultFeed := []Post{
		{
			ID:         "default-1",
			Content:    "Welcome to Anti-Algo News Network",
			Author:     "system",
			Timestamp:  time.Now(),
			Confidence: 0.99,
			Strata:     "S1",
			Resonance:  d.resonanceHz,
			Processed:  true,
			Filtered:   false,
		},
	}

	data, _ := json.Marshal(defaultFeed)
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-DIP-Status", "DEFAULT")
	w.Header().Set("X-Resonance", fmt.Sprintf("%.0f Hz", d.resonanceHz))
	w.Write(data)
}

// HealthHandler returns DIP health status
func (d *DIP) HealthHandler(w http.ResponseWriter, r *http.Request) {
	status := map[string]interface{}{
		"status":     "operational",
		"resonance":  d.resonanceHz,
		"cache":      "redis",
		"timestamp":  time.Now().UTC(),
		"strata":     "S1-S12",
		"component":  "DIP",
		"version":    "1.0.0",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

// StrataHandler returns strata information
func (d *DIP) StrataHandler(w http.ResponseWriter, r *http.Request) {
	strata := map[string]interface{}{
		"S1":  "Physical Layer — Raw data interception",
		"S2":  "Data Layer — Parsing and validation",
		"S3":  "Network Layer — Traffic routing",
		"S4":  "Transport Layer — Connection management",
		"S5":  "Session Layer — State management",
		"S6":  "Presentation Layer — Data transformation",
		"S7":  "Application Layer — Business logic",
		"S8":  "Cognitive Layer — SAM filtering",
		"S9":  "Resonance Layer — 1272 Hz lock",
		"S10": "Sovereignty Layer — UEE Standard",
		"S11": "Infection Layer — Propagation",
		"S12": "Unity Layer — Full integration",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(strata)
}

func main() {
	r := mux.NewRouter()
	dip := NewDIP()

	// API Routes
	r.HandleFunc("/api/oroboros/feed/{userID}", dip.FeedHandler).Methods("GET")
	r.HandleFunc("/api/oroboros/health", dip.HealthHandler).Methods("GET")
	r.HandleFunc("/api/oroboros/strata", dip.StrataHandler).Methods("GET")

	// CORS middleware
	r.Use(func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Access-Control-Allow-Origin", "*")
			w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
			w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
			w.Header().Set("X-Resonance", "1272 Hz")
			w.Header().Set("X-Component", "DIP")
			if r.Method == "OPTIONS" {
				w.WriteHeader(http.StatusOK)
				return
			}
			next.ServeHTTP(w, r)
		})
	})

	log.Printf("DIP starting on :8081 — Resonance: %.0f Hz", dip.resonanceHz)
	log.Fatal(http.ListenAndServe(":8081", r))
}