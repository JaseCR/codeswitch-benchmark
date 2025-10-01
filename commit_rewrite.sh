#!/bin/bash

# Rewrite commit messages based on content patterns
git filter-branch -f --msg-filter '
    # Read the original commit message
    read -r msg
    
    # Rewrite based on content patterns
    case "$msg" in
        *"Initial setup"*)
            echo "Initial setup → set up the repo and first file structure for the code-switching benchmark project."
            ;;
        *"Code-switching benchmark backend and visualizations"*)
            echo "Code-switching benchmark backend and visualizations → built the main structure for running tests and added basic plotting functions."
            ;;
        *"Implement OpenAI adapter"*)
            echo "Implement OpenAI adapter with config options → added an OpenAI adapter that lets me swap models easily and test consistency."
            ;;
        *"Optimize for OpenAI Pro access"*)
            echo "Optimize for OpenAI Pro access → cleaned up API setup so I can use my Pro access more efficiently."
            ;;
        *"Add quota troubleshooting"*)
            echo "Add quota troubleshooting + fallback tools → added a quick workaround for when I hit rate limits or token errors."
            ;;
        *"Optimize again for OpenAI Pro access"*)
            echo "Optimize again for OpenAI Pro access → fixed small bugs and made sure token tracking works right across runs."
            ;;
        *"Implement Claude"*)
            echo "Implement Claude (Anthropic) adapter → wrote a separate class for Anthropic models so I can test Claude alongside GPT."
            ;;
        *"Add Cohere adapter"*)
            echo "Add Cohere adapter + debugging tools → built out Cohere integration and added print/debug logs to test responses."
            ;;
        *"Remove old Anthropic integration"*)
            echo "Remove old Anthropic integration → cleaned up duplicate code from early versions of the Claude adapter."
            ;;
        *"Add Mistral integration"*)
            echo "Add Mistral integration → started testing Mistral models for comparison—added basic wrapper code."
            ;;
        *"Add note about Mistral integration"*)
            echo "Add note about Mistral integration → small doc update just explaining how the Mistral setup works."
            ;;
        *"Add background agent"*)
            echo "Add background agent + clean up .env file → added a small background helper for local runs and fixed the env file format."
            ;;
        *"Add advanced visualizations"*)
            echo "Add advanced visualizations for EDA → built extra charts to show model differences more clearly (length, overlap, markers)."
            ;;
        *"Simplify visualization code"*)
            echo "Simplify visualization code for readability → refactored plots so they're easier to understand and re-use later."
            ;;
        *"Streamline visuals for accessibility"*)
            echo "Streamline visuals for accessibility → made color palettes and labels more readable (for presentations too)."
            ;;
        *"Fix ValueError in Gemini analysis"*)
            echo "Fix ValueError in Gemini analysis → fixed a bug that broke the Gemini chart generation step."
            ;;
        *"Replace pie chart with bar chart"*)
            echo "Replace pie chart with bar chart → swapped out a bad pie chart for a clearer bar graph version."
            ;;
        *"Correct Gemini data source"*)
            echo "Correct Gemini data source → fixed a path issue that was loading the wrong file for the Gemini dataset."
            ;;
        *"Replace problematic Gemini analysis"*)
            echo "Replace problematic Gemini analysis with summary → cleaned up the code and replaced broken plots with a quick data summary."
            ;;
        *"Remove redundant test notebooks"*)
            echo "Remove redundant test notebooks → deleted a few duplicates and old scratch notebooks."
            ;;
        *"Create clean, professional EDA notebook"*)
            echo "Create clean, professional EDA notebook → finalized the EDA notebook for presentation—plots, questions, and narrative all in one."
            ;;
        *)
            # Keep original message if no pattern matches
            echo "$msg"
            ;;
    esac
' --all
