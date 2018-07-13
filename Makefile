DIR_IMG := img

images := $(patsubst %.py,%.png,$(wildcard *.py))
images := $(foreach img,$(images),$(DIR_IMG)/$(img))

all: dirs $(images)

dirs:
	@[ -d "$(DIR_IMG)" ] || mkdir "$(DIR_IMG)"

$(DIR_IMG)/%.png: %.py dims.toml
	blender --background --python $< -- img_dir=$(DIR_IMG)
