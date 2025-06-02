
# mini-cursor

**mini-cursor** is a lightweight AI-powered code agent designed to assist developers by providing intelligent code suggestions and automating routine coding tasks. Built with Python, it leverages advanced language models to enhance productivity and streamline the development workflow.

## Features

- **AI-Powered Code Suggestions**: Utilizes advanced language models to provide context-aware code completions and recommendations.
- **Customizable System Prompts**: Tailor the behavior of the code agent by modifying the `system_prompt.txt` file to suit specific project needs.
- **Lightweight and Efficient**: Designed to be minimalistic, ensuring quick setup and seamless integration into existing projects.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key (or compatible API key for the language model you intend to use)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Gaurav-04-06/mini-cursor.git
   cd mini-cursor
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   Create a `.env` file in the root directory and add your API key:

   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the code agent using the following command:

```bash
python code-agent.py
```

The agent will initialize and be ready to assist with code suggestions based on the context provided.

## Customization

- **System Prompt**: Modify the `system_prompt.txt` file to change the initial instructions or behavior of the AI model. This allows for customization of the agent's responses to better fit your project's requirements.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the capabilities of AI-assisted coding tools and the desire to create a minimalistic alternative.
- Thanks to the open-source community for continuous support and inspiration.
