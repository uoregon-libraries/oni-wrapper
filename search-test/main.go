package main

import (
	"fmt"
	"math/rand"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// Subset of the Dolch list nouns.  These are some of the most common English
// words.  We choose five of these randomly and perform an "or" search.
var words = []string{
	"apple", "baby", "back", "ball", "bear", "bed", "bell", "bird", "birthday", "boat",
	"box", "boy", "bread", "brother", "cake", "car", "cat", "chair", "chicken", "children",
	"coat", "corn", "cow", "day", "dog", "doll", "door", "duck", "egg", "eye",
	"farm", "farmer", "father", "feet", "fire", "fish", "floor", "flower", "game", "garden",
	"girl", "grass", "ground", "hand", "head", "hill", "home", "horse", "house",
	"kitty", "leg", "letter", "man", "men", "milk", "money", "morning", "mother", "name",
	"nest", "night", "paper", "party", "picture", "pig", "rabbit", "rain", "ring", "robin",
	"school", "seed", "sheep", "shoe", "sister", "snow", "song", "squirrel", "stick", "street",
	"sun", "table", "thing", "time", "top", "toy", "tree", "watch", "water", "way",
	"wind", "window", "wood",
}

// We always expect at least triple-digit results.  With five random, common
// words, it is basicaly impossible to not have a lot of results in production
// or staging.
var searchRE = regexp.MustCompile(`\s+(\d\d\d+) results\s+containing`)

func main() {
	var info statusInfo

	var args = getArgs()
	info.Words = randomWords(5)
	info.URL = makeSearchURL(args.url, info.Words)
	info.Error = ""

	info.get()
	if info.Error != "" {
		info.Print(os.Stderr)
		os.Exit(1)
	}

	var matches = searchRE.FindSubmatch(info.ResponseBody)
	if len(matches) != 2 {
		info.Error = "no search results found by regexp"
		info.Print(os.Stderr)
		os.Exit(1)
	}

	info.Success = true
	if args.printBody {
		fmt.Println(string(info.ResponseBody))
	}

	// Ignore the error from Atoi since the regex already forces digit-only input
	info.ResultCount, _ = strconv.ParseInt(string(matches[1]), 10, 64)
	info.Print(os.Stdout)
}

func randomWords(n int) string {
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(words), func(i, j int) {
		words[i], words[j] = words[j], words[i]
	})

	return strings.Join(words[:n], " ")
}

func makeSearchURL(base *url.URL, query string) string {
	// Yes it's stupid to re-parse the URL just to create a new one, but it's
	// effective and ensures a perfect clone including user/pass if they exist
	var newU, _ = url.Parse(base.String())

	var vals = newU.Query()
	vals.Set("ortext", query)
	vals.Set("andtext", "")
	vals.Set("phrasetext", "")
	vals.Set("proxtext", "")
	vals.Set("proxdistance", "5")
	vals.Set("city", "")
	vals.Set("county", "")
	vals.Set("date1", "1846-01-01")
	vals.Set("date2", "2020-12-31")
	vals.Set("language", "")
	vals.Set("frequency", "")
	vals.Set("rows", "20")
	vals.Set("searchType", "advanced")

	newU.RawQuery = vals.Encode()
	return newU.String()
}
