# ChronoFlux - Time-Inspired AI Image Generation

A sleek and user-friendly Streamlit interface for Black Forest Labs' Flux AI image generation API. Create stunning AI-generated images with time-inspired prompts and advanced controls.

![ChronoFlux Screenshot](docs/screenshot.png)

## Features

- 🎨 Simple and intuitive user interface
- ✨ Advanced image generation controls
- 📐 Multiple aspect ratio presets
- 🎯 Fine-tuned image quality settings
- 🚫 Negative prompt support
- 🎲 Seed control for reproducible results
- 🔄 Multiple sampling methods

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Black Forest Labs API key ([Get one here](https://bfl.ai))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chronoflux.git
cd chronoflux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Create a `.env` file in the project root
   - Add your API key: `FLUX_API_KEY=your_api_key_here`

4. Run the app:
```bash
streamlit run streamlit_app.py
```

## Example

Here's a fun example of what you can create with ChronoFlux:

![Cat Choir](docs/example_cats.jpg)

Prompt used:
```
A large group of cats singing in a choir, all looking up with open mouths, mixture of orange, white, and black cats, soft lighting, high quality, detailed fur, expressive faces, cozy blanket
```

Negative prompt:
```
blurry, low quality, distorted, unrealistic, bad anatomy
```

Settings used:
- Sampler: euler_a
- Steps: 35
- Guidance Scale: 7.0
- Aspect Ratio: Landscape (4:3)

## Usage

1. Enter your prompt in the text area
2. (Optional) Configure advanced settings:
   - Image Quality:
     - Quality Steps (20-50)
     - Creativity vs Precision
     - Sampling Method
     - Random Seed
   - Image Content:
     - Negative Prompt
     - Aspect Ratio

3. Click "Generate Image" and wait for your creation!

## Advanced Settings Explained

### Quality Settings

- **Quality Steps**: Higher values (20-50) produce better quality but take longer
- **Creativity vs Precision**: Lower values (0-10) give more creative results
- **Sampling Method**:
  - euler_a: Fast and good quality (default)
  - euler: Similar to euler_a
  - heun: High quality but slower
  - dpm_2: Good for detailed images
  - dpm_2_a: Variant of dpm_2
  - lms: Linear multistep method

### Content Settings

- **Negative Prompt**: Specify what you don't want in the image
- **Aspect Ratio**:
  - Square (1:1) - 1024x1024
  - Portrait (3:4) - 768x1024
  - Landscape (4:3) - 1024x768
  - Wide (16:9) - 1024x576
  - Tall (9:16) - 576x1024

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Black Forest Labs](https://bfl.ai) for their amazing Flux API
- [Streamlit](https://streamlit.io) for the awesome web framework

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/chronoflux/issues) on GitHub.
