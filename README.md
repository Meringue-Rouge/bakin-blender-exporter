# bakin-blender-exporter
![image](https://github.com/user-attachments/assets/23f51664-bfe6-49ba-a63d-a09acf8ba78d)

## ENGLISH

**A Blender Addon that allows you to quickly export (in a single-click) FBX models and their material definitions (.def files) for RPG Developer BAKIN, letting you easily import your models into Bakin without having to manually import every texture for every model!**

Version 2.0 is a major update that aims to make the Bakin Model Exporter handle a LOT more features than before, including a new UI, and more utility, hopefully making model importing much more reliable in RPG Developer Bakin.

> [!TIP]
> If you wish to import a VRM model from VRoid Studio in RPG Developer Bakin, use this Blender add-on instead: https://github.com/Meringue-Rouge/bakin-vrm-blender

### Features
- Makes your model import into RPG Developer Bakin without (hopefully) having to manually assign textures / properties!
  - Exports your model, textures, and a material definition file (.def) in a single folder.
- **_Triangulation Check & Fix:_** Detects if there are any meshes that are not triangulated, and will add a Triangulate modifier to the meshes. If the model looks untextured and broken in Bakin while popping error messages, press this button and export again.
- **_(BETA) Generate Missing Textures from Albedo:_** Each material has an indicator for each texture field that Bakin can use. If you press one of the texture fields that is in red, the addon will ask you if it should generate and assign that texture for the selected material. (Results might not be correct, hence beta for now)
- **_Bakin Material Properties:_** Several (but not all) of the properties that can be edited in Bakin, such as shader type, outline settings, receiving decals, and more, can be edited straight from the addon, per material, and Bakin will immediately apply the correct settings upon importing.
- **Generates Mask Maps** according to BAKIN's specifications from the model's Shader Node textures: Roughness, Metallic, Emissive and Specular.
- Language support for English, Japanese (AI-translated) and Simplified Chinese (AI-translated).

> [!CAUTION]
> Due to the nature of 3D Models and especially Materials, the add-on won't guarantee your model will import in RPG Developer Bakin without issues. Always check your shader nodes in Blender (especially if you're downloading models off the internet), textures, filenames, and try again.

### Usage
- Install the blender add-on by going to Edit -> Preferences, going to Add-ons, and selecting in the top-right the Install from Disk option (hidden in a small square on 4.2+)
  - On older versions of Blender, make sure to tick the box to enable the add-on.
- You'll find the Add-on on the right menu, which can be opened by pressing N, or clicking on the little arrow.
- Make sure your model uses Principled BSDF shader nodes (PBR), and save the blend file project.
- Make sure your texture nodes in the shader nodes connect to the standard inputs.
- Define a model name in the addon. This will define the folder name, model filename, and def filename, and will be saved in the folder where your blend file is.
- Press "Export FBX+DEF".
- Import the model into RPG Developer BAKIN.

### Credits
- Models shown are from Blenderkit (https://www.blenderkit.com/)
- Code was (mostly) generated through ChatGPT (with a lot of troubleshooting and fixing), and Grok for version 2.

## 日本語

**RPGデベロッパーBAKIN用のFBXモデルとそのマテリアル定義（.defファイル）を素早く（ワンクリックで）エクスポートできるBlenderアドオンです。**

バージョン2.0は、Bakin Model Exporterが新しいUIやより多くのユーティリティを含む、以前よりも多くの機能を扱えるようにすることを目的としたメジャー・アップデートで、RPG Developer Bakinでのモデルのインポートがより信頼できるものになることを期待しています。

> [!TIP]
> RPG Developer BakinでVRoid StudioからVRMモデルをインポートしたい場合は、代わりにこのBlenderアドオンを使用してください： https://github.com/Meringue-Rouge/bakin-vrm-blender

### 特徴
- テクスチャやプロパティを手動で割り当てることなく、モデルをRPG Developer Bakinにインポートできます！
  - モデル、テクスチャ、マテリアル定義ファイル(.def)を1つのフォルダにエクスポートします。
- 三角形化チェックと修正:_** 三角形化されていないメッシュがあるかどうかを検出し、そのメッシュにTriangulateモディファイアを追加します。 Bakinでモデルがテクスチャ化されておらず、エラーメッセージが表示されながら壊れているように見える場合は、このボタンを押して再度エクスポートしてください。
- 各マテリアルには、Bakinが使用できる各テクスチャフィールドのインジケータがあります。 赤で表示されているテクスチャフィールドの1つを押すと、アドオンは選択したマテリアルにそのテクスチャを生成して割り当てるべきかどうかを尋ねます。 (結果は正しくないかもしれないので、今のところベータ版です)
- Bakin Material Properties:_**シェーダタイプ、アウトライン設定、受信デカールなど、Bakinで編集できるプロパティのいくつか（すべてではありません）は、マテリアルごとにアドオンから直接編集でき、Bakinはインポート時にすぐに正しい設定を適用します。
- モデルのシェーダーノードテクスチャからBAKINの仕様に従ってマスクマップ**を生成します： ラフネス、メタリック、エミッシブ、スペキュラ。
- 英語、日本語（AI翻訳）、簡体字中国語（AI翻訳）をサポート。

> [!CAUTION]
> 3Dモデルと特にマテリアルの性質上、アドオンはあなたのモデルが問題なくRPG Developer Bakinにインポートされることを保証するものではありません。 Blenderのシェーダノード（特にインターネットからモデルをダウンロードしている場合）、テクスチャ、ファイル名を常にチェックし、もう一度試してみてください。

### 使用方法
- Edit -> PreferencesでAdd-onsを選択し、右上のInstall from Diskオプションを選択してBlenderアドオンをインストールします（4.2+では小さな四角の中に隠れています）。
  - 古いバージョンのBlenderでは、アドオンを有効にするボックスにチェックを入れてください。
- アドオンは右メニューにあり、Nを押すか、小さな矢印をクリックすると開きます。
- モデルがPrincipled BSDFシェーダノード（PBR）を使用していることを確認し、ブレンドファイルのプロジェクトを保存します。
- シェーダノードのテクスチャノードが標準入力に接続されていることを確認してください。
- アドオンでモデル名を定義します。 これは、フォルダ名、モデルファイル名、defファイル名を定義し、ブレンドファイルがあるフォルダに保存されます。
- Export FBX+DEF "を押す。
- モデルをRPG Developer BAKINにインポートする。

### クレジット
- モデルはBlenderkit (https://www.blenderkit.com/) のものです。
- コードは(ほとんど)ChatGPTで生成され(トラブルシューティングと修正が多かった)、バージョン2ではGrokを使用した。
