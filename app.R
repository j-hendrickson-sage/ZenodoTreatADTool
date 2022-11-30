library(DT)
library(shiny)
library(reticulate)

reticulate::virtualenv_create(envname = 'python3_env')
reticulate::virtualenv_install('python3_env', packages = c('requests', "pandas"))

ui <- basicPage(
  h2("The TREAT-AD Community Data"),
  DT::dataTableOutput("mytable"),
  fluidPage(
    actionButton("action", label = "pullData"),
    uiOutput("downloadData")
  )
)

server <- function(input, output) {
  reticulate::use_virtualenv('python3_env', required = T)
  reticulate::source_python("requestData.py")
  
  df <- reactive({
    response <- getResponse()
    requestData(response)
  }) %>%
    bindEvent(input$action)
  
  output$mytable = DT::renderDataTable({
    df()
  })
  
  output$downloadData <- renderUI({
    req(input$action, df())
    downloadButton("downloadData01")
  })
  
  output$downloadData01 <- downloadHandler(
    filename = function() {
      paste0(Sys.time(), "_TREATAD_Zenodo.csv")
    },
    content = function(fname) {
      write.csv(df(), fname)
    }
  )
}

shinyApp(ui, server)